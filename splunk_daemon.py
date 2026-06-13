import time
import asyncio
from loguru import logger
import socket
import threading
import json
from collections import Counter, deque

from src.mcp_tools.auth_tools import AuthTools
from src.mcp_tools.network_tools import NetworkTools
from src.mcp_tools.security_tools import SecurityTools
from src.mcp_tools.system_tools import SystemTools

from src.anomaly.analyzer import AnomalyAnalyzer
from src.intelligence.engine import IntelligenceEngine
from src.alerts.global_alerts import GlobalAlertStore

POLL_INTERVAL = 10

# Rolling history length per bucket (used to build real baseline)
HISTORY_SIZE = 20


class SplunkDaemon:

    def __init__(self):
        self.clients_lock = threading.Lock()
        self._setup_ram_log_streamer()

        self.auth     = AuthTools()
        self.network  = NetworkTools()
        self.security = SecurityTools()
        self.system   = SystemTools()

        self.anomaly_engine = AnomalyAnalyzer()
        self.intel_engine   = IntelligenceEngine()

        # FIX 1: Per-bucket rolling history so baseline grows from real data
        self.history: dict[str, deque] = {
            "auth":     deque(maxlen=HISTORY_SIZE),
            "network":  deque(maxlen=HISTORY_SIZE),
            "security": deque(maxlen=HISTORY_SIZE),
            "system":   deque(maxlen=HISTORY_SIZE),
        }

    # =====================================================
    # RAM LOG STREAMER
    # =====================================================
    def _setup_ram_log_streamer(self):
        """Sets up an in-memory network socket to broadcast logs over RAM."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("127.0.0.1", 5555))
        self.server_socket.listen(5)
        self.clients: list = []

        threading.Thread(target=self._accept_connections, daemon=True).start()
        logger.add(
            self._broadcast_log,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}\n",
        )

    def _accept_connections(self):
        while True:
            try:
                client_sock, _ = self.server_socket.accept()
                with self.clients_lock:
                    self.clients.append(client_sock)
            except Exception:
                break

    def _broadcast_log(self, message):
        """Broadcasts the log string across the volatile RAM socket layer."""
        log_entry = str(message)
        print(log_entry, end="")

        with self.clients_lock:
            for client in list(self.clients):
                try:
                    client.sendall((log_entry + "\n").encode("utf-8"))
                except Exception:
                    self.clients.remove(client)

    # =====================================================
    # HELPERS
    # =====================================================
    @staticmethod
    def _unpack_event(e: dict) -> dict:
        """
        FIX 2: Safely unwrap the Supabase 'event' JSONB column.
        Handles both pre-parsed dicts and raw JSON strings.
        Top-level row fields take priority over nested event fields
        so that attack_type / severity from the schema are never
        overwritten by whatever is inside the JSONB blob.
        """
        inner = e.get("event") or e.get("payload") or e.get("metadata") or {}

        if isinstance(inner, str):
            try:
                inner = json.loads(inner)
            except (ValueError, TypeError):
                inner = {}

        if not isinstance(inner, dict):
            inner = {}

        # Merge: inner fields first, top-level schema fields win on collision
        return {**inner, **e}

    @staticmethod
    def _route_event(normalized: dict) -> str:
        """
        FIX 3: Route purely on attack_type (always populated in your schema).
        Removed the broken `or attack_type` truthy gate that was sending
        everything into the soc_sim branch regardless of content.
        """
        attack_type = str(
            normalized.get("attack_type")
            or normalized.get("attackType")
            or normalized.get("incident_type")
            or ""
        ).lower()

        src = str(normalized.get("source", "system")).lower()

        # Route by attack_type first (most specific)
        if "brute" in attack_type or "credential" in attack_type or "auth" in attack_type:
            return "auth"
        if (
            "ddos"    in attack_type
            or "scan"    in attack_type
            or "network" in attack_type
            or "port"    in attack_type
            or "flood"   in attack_type
        ):
            return "network"
        if (
            "inject" in attack_type
            or "xss"    in attack_type
            or "sqli"   in attack_type
            or "rce"    in attack_type
            or "lfi"    in attack_type
        ):
            return "security"
        if (
            "error"    in attack_type
            or "crash"   in attack_type
            or "fail"    in attack_type
            or "overflow" in attack_type
        ):
            return "system"

        # Fallback: route by source channel
        if "auth"     in src:
            return "auth"
        if "network"  in src:
            return "network"
        if "security" in src:
            return "security"

        return "security"   # safe default — not "system"

    def _build_spike_series(self, name: str, valid: list) -> list:
        """
        FIX 4: Build a meaningful anomaly series instead of count=1 for every event.

        Strategy:
          - The current cycle's event count is the spike value.
          - The rolling history of past cycle counts forms the baseline.
          - If history is short, pad with 1s (quiet baseline assumption).
          - This gives detectors a real signal: [1,1,2,1,1,19] → clear spike.
        """
        spike_value = len(valid)

        # Append current count to history BEFORE building series
        self.history[name].append(spike_value)

        history_list = list(self.history[name])

        # Need at least 10 points for analyze_series; pad with 1s if cold start
        baseline = history_list[:-1]  # everything except the current cycle
        while len(baseline) < 9:
            baseline.insert(0, 1)

        series = baseline + [spike_value]

        logger.info(
            f"[{name}] Series → baseline_tail={baseline[-3:]} spike={spike_value} "
            f"series_len={len(series)}"
        )
        return series

    # =====================================================
    # PARALLEL EVENT COLLECTION
    # =====================================================
    async def collect_events_async(self) -> list:
        logger.info("⚡ Starting parallel MCP collection")
        loop = asyncio.get_running_loop()

        tasks = [
            loop.run_in_executor(None, self.auth.get_auth_logs),
            loop.run_in_executor(None, self.network.get_network_logs),
            loop.run_in_executor(None, self.security.get_auth_logs),
            loop.run_in_executor(None, self.system.get_system_logs),
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)
        events: list = []

        for r in results:
            if isinstance(r, Exception):
                logger.error(f"❌ MCP tool failed: {r}")
                continue
            if isinstance(r, list):
                events.extend(r)

        logger.info(f"📦 Parallel MCP collection complete: {len(events)} events")

        # Supabase ingestion
        try:
            from src.storage.attack_log_store import AttackLogStore
            cloud_logs = AttackLogStore.get_all()
            logger.info(f"☁️ Retrieved {len(cloud_logs)} cloud logs from Supabase")
            if cloud_logs:
                events.extend(cloud_logs)
                # ids = [row["id"] for row in cloud_logs if "id" in row]
                # if ids:
                #     AttackLogStore.delete_batch(ids)
        except Exception as e:
            logger.error(f"Supabase ingestion error: {e}")

        return events

    # =====================================================
    # PARALLEL ANOMALY ANALYSIS
    # =====================================================
    async def run_anomaly_parallel(self, grouped: dict) -> list:
        logger.info("⚡ Running parallel anomaly detection")
        loop = asyncio.get_running_loop()

        tasks = []
        meta  = []

        for name, group in grouped.items():
            if not group:
                continue

            # FIX 5: Skip non-dict entries cleanly
            valid = [x for x in group if isinstance(x, dict)]
            if not valid:
                continue

            # FIX 4 (applied): build real spike series from rolling history
            values = self._build_spike_series(name, valid)

            meta.append((name, valid))
            tasks.append(
                loop.run_in_executor(
                    None,
                    self.anomaly_engine.analyze_series,
                    name,
                    values,
                    valid,
                )
            )

        if not tasks:
            logger.warning("No valid buckets to analyze this cycle")
            return []

        results = await asyncio.gather(*tasks, return_exceptions=True)
        threats = []

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Anomaly task failed: {result}")
                continue
            if not result:
                continue

            threats.append(result)

            # Push global alert
            try:
                bucket_name, raw_events = meta[i]
                await GlobalAlertStore.push_alert({
                    "title":         f"Anomaly detected in {bucket_name}",
                    "severity":      result.severity,
                    "attack_type":   result.attack_type,
                    "summary":       result.description,
                    "source_events": len(raw_events),
                })
            except Exception as e:
                logger.error(f"Alert push failed: {e}")

        logger.info(f"🚨 Detected {len(threats)} anomalies this cycle")
        return threats

    # =====================================================
    # MAIN CYCLE
    # =====================================================
    async def run_cycle(self) -> dict:
        logger.info("🔄 Starting collection cycle")
        events = await self.collect_events_async()
        logger.info(f"📊 Total events collected: {len(events)}")

        grouped: dict[str, list] = {
            "auth":     [],
            "network":  [],
            "security": [],
            "system":   [],
        }

        for e in events:
            if not isinstance(e, dict):
                # FIX 6: drop non-dict entries instead of dumping to system
                logger.debug(f"Skipping non-dict event: {type(e)}")
                continue

            normalized = self._unpack_event(e)   # FIX 2
            bucket     = self._route_event(normalized)  # FIX 3
            grouped[bucket].append(normalized)

        logger.info(
            f"Bucket distribution → "
            f"Auth: {len(grouped['auth'])} | "
            f"Net: {len(grouped['network'])} | "
            f"Sec: {len(grouped['security'])} | "
            f"Sys: {len(grouped['system'])}"
        )

        threats = await self.run_anomaly_parallel(grouped)
        reports = self.intel_engine.analyze(threats)
        logger.info(f"🧠 Generated {len(reports)} intelligence reports")

        return {
            "events":  len(events),
            "threats": len(threats),
            "reports": len(reports),
        }

    # =====================================================
    # DAEMON LOOP
    # =====================================================
    async def run(self):
        logger.info("🚀 SentinelAI Daemon Started")

        while True:
            try:
                start  = time.time()
                result = await self.run_cycle()
                elapsed = time.time() - start
                logger.info(f"⏱️ Cycle completed in {elapsed:.2f}s")
                logger.info(f"📊 Summary: {result}")
            except Exception as e:
                logger.exception(f"Daemon cycle error: {e}")

            await asyncio.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    asyncio.run(SplunkDaemon().run())