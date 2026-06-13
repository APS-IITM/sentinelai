import time
import asyncio
from loguru import logger
import socket
import threading

from src.mcp_tools.auth_tools import AuthTools
from src.mcp_tools.network_tools import NetworkTools
from src.mcp_tools.security_tools import SecurityTools
from src.mcp_tools.system_tools import SystemTools

from src.anomaly.analyzer import AnomalyAnalyzer
from src.intelligence.engine import IntelligenceEngine
from src.alerts.global_alerts import GlobalAlertStore

POLL_INTERVAL = 10

class SplunkDaemon:

    def __init__(self):
        # 1. Thread-safe lock for clients list
        self.clients_lock = threading.Lock()
        self._setup_ram_log_streamer()

        self.auth = AuthTools()
        self.network = NetworkTools()
        self.security = SecurityTools()
        self.system = SystemTools()

        self.anomaly_engine = AnomalyAnalyzer()
        self.intel_engine = IntelligenceEngine()
    
    def _setup_ram_log_streamer(self):
        """Sets up an in-memory network socket to broadcast logs over RAM."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.server_socket.bind(('127.0.0.1', 5555))
        self.server_socket.listen(5)
        self.clients = []

        threading.Thread(target=self._accept_connections, daemon=True).start()
        logger.add(self._broadcast_log, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}\n")
    
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
        
        # Safe iteration with Lock
        with self.clients_lock:
            for client in list(self.clients):
                try:
                    client.sendall((log_entry + "\n").encode("utf-8"))
                except Exception:
                    self.clients.remove(client)
      
    # =====================================================
    # PARALLEL EVENT COLLECTION 
    # =====================================================
    async def collect_events_async(self):
        logger.info("⚡ Starting parallel MCP collection")
        loop = asyncio.get_running_loop()

        tasks = [
            loop.run_in_executor(None, self.auth.get_auth_logs),
            loop.run_in_executor(None, self.network.get_network_logs),
            loop.run_in_executor(None, self.security.get_auth_logs),
            loop.run_in_executor(None, self.system.get_system_logs),
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)
        events = []

        for r in results:
            if isinstance(r, Exception):
                logger.error(f"❌ MCP tool failed: {r}")
                continue
            if isinstance(r, list):
                events.extend(r)

        logger.info(f"📦 Parallel collection complete: {len(events)} events")

        # Supabase ingestion
        try:
            from src.storage.attack_log_store import AttackLogStore
            cloud_logs = AttackLogStore.get_all()
            logger.info(f"☁️ Retrieved {len(cloud_logs)} cloud logs from Supabase")
            if cloud_logs:
                events.extend(cloud_logs)
                ids = [row["id"] for row in cloud_logs if "id" in row]
                #if ids:
                   # AttackLogStore.delete_batch(ids)
        except Exception as e:
            logger.error(f"Supabase error: {e}")

        return events

    # =====================================================
    # PARALLEL ANOMALY ANALYSIS (MADE ASYNC NATIVE)
    # =====================================================
    async def run_anomaly_parallel(self, grouped):
        logger.info("⚡ Running parallel anomaly detection")
        loop = asyncio.get_running_loop()

        tasks = []
        meta = []

        for name, group in grouped.items():
            if not group:
                continue

            valid = [x for x in group if isinstance(x, dict)]
            if not valid:
                continue

            values = [
                int(x.get("count", 1)) if isinstance(x, dict) else 1
                for x in valid
            ]

            while len(values) < 10:
                values.insert(0, 1)

            meta.append((name, valid))

            # Dispatch synchronous engine code securely to the executor pool
            tasks.append(
                loop.run_in_executor(
                    None,
                    self.anomaly_engine.analyze_series,
                    name,
                    values,
                    valid
                )
            )

        if not tasks:
            return []

        results = await asyncio.gather(*tasks)
        threats = []

        for i, result in enumerate(results):
            if not result:
                continue

            threats.append(result)

            # 🚨 GLOBAL ALERT TRIGGER (Now safely parsing object fields)
            try:
                name, raw_events = meta[i]
                await GlobalAlertStore.push_alert({
                    "title": f"Anomaly detected in {name}",
                    "severity": result.severity, # Access property directly
                    "attack_type": result.attack_type, 
                    "summary": result.description, 
                    "source_events": len(raw_events)
                })
            except Exception as e:
                logger.error(f"Alert push failed: {e}")
                
        logger.info(f"🚨 Detected {len(threats)} anomalies")
        return threats

    # =====================================================
    # MAIN CYCLE (ASYNC)
    # =====================================================
    async def run_cycle(self):
        logger.info("🔄 Starting collection cycle")
        events = await self.collect_events_async()
        logger.info(f"📊 Collected {len(events)} events")

        grouped = {"auth": [], "network": [], "security": [], "system": []}

        for e in events:
            if not isinstance(e, dict):
                grouped["system"].append(e)
                continue

            # --- HARDENED NORMALIZATION ---
            # Extract nested fields even if Supabase doesn't use the specific key "event"
            payload = e.get("event") or e.get("payload") or e.get("metadata") or {}
            if not isinstance(payload, dict):
                payload = {}
            
            normalized = {**e, **payload}

            # Debug check: Un-comment this line if you need to see exactly what fields are arriving
            # logger.debug(f"Normalized keys: {list(normalized.keys())}")

            src = str(normalized.get("source", "system")).lower()
            
            # Catch attack types regardless of key casing
            attack_type = str(
                normalized.get("attack_type") or 
                normalized.get("attackType") or 
                normalized.get("incident_type", "")
            ).lower()

            # --- TARGETED ROUTING ---
            if "soc_sim" in src or attack_type or "sim" in src:
                if "brute" in attack_type or "auth" in attack_type:
                    grouped["auth"].append(normalized)
                elif "ddos" in attack_type or "scan" in attack_type or "network" in attack_type:
                    grouped["network"].append(normalized)
                elif "error" in attack_type or "fail" in attack_type:
                    grouped["system"].append(normalized)
                else:
                    grouped["security"].append(normalized)
            else:
                if "auth" in src:
                    grouped["auth"].append(normalized)
                elif "network" in src:
                    grouped["network"].append(normalized)
                elif "security" in src:
                    grouped["security"].append(normalized)
                else:
                    grouped["system"].append(normalized)

        # Print snapshot of bucket counts to make sure they aren't all landing in system
        logger.info(f"Bucket Distribution -> Auth: {len(grouped['auth'])} | Net: {len(grouped['network'])} | Sec: {len(grouped['security'])} | Sys: {len(grouped['system'])}")

        threats = await self.run_anomaly_parallel(grouped)
        reports = self.intel_engine.analyze(threats)
        logger.info(f"🧠 Generated {len(reports)} intelligence reports")

        return {
            "events": len(events),
            "threats": len(threats),
            "reports": len(reports)
        }
    
    # =====================================================
    # DAEMON LOOP (ASYNC)
    # =====================================================
    async def run(self):
        logger.info("🚀 SentinelAI Daemon Started")

        while True:
            try:
                start = time.time()
                result = await self.run_cycle()
                logger.info(f"⏱️ Cycle completed in {time.time() - start:.2f}s")
                logger.info(f"📊 Summary: {result}")
            except Exception as e:
                logger.exception(f"Daemon error: {e}")

            await asyncio.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    # Start the event loop cleanly from the main execution point
    asyncio.run(SplunkDaemon().run())