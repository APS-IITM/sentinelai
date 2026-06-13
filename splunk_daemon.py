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
        # 1. Remove the file logger and replace it with a Socket Streamer
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
        
        # Bind to localhost on an arbitrary free port (e.g., 5555)
        self.server_socket.bind(('127.0.0.1', 5555))
        self.server_socket.listen(5)
        self.clients = []

        # Run the socket listener in a background thread so it doesn't block the daemon loop
        threading.Thread(target=self._accept_connections, daemon=True).start()

        # Tell Loguru to pipe all logs directly to our broadcast function
        logger.add(self._broadcast_log, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
    
    def _accept_connections(self):
        while True:
            try:
                client_sock, _ = self.server_socket.accept()
                self.clients.append(client_sock)
            except Exception:
                break

    def _broadcast_log(self, message):
        """Broadcasts the log string across the volatile RAM socket layer."""
        log_entry = str(message)
        # Print to terminal window normally
        print(log_entry, end="") 
        
        # Send to Streamlit over memory loopback
        for client in list(self.clients):
            try:
                client.sendall(log_entry.encode('utf-8'))
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

        # Supabase ingestion (still sync, optional optimization later)
        try:
            from src.storage.attack_log_store import AttackLogStore

            cloud_logs = AttackLogStore.get_all()

            if cloud_logs:
                events.extend(cloud_logs)

                ids = [row["id"] for row in cloud_logs if "id" in row]
                if ids:
                    AttackLogStore.delete_batch(ids)

        except Exception as e:
            logger.error(f"Supabase error: {e}")

        return events

    # =====================================================
    # PARALLEL ANOMALY ANALYSIS 
    # =====================================================
    

    def run_anomaly_parallel(self, grouped):
        logger.info("⚡ Running parallel anomaly detection")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

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

            # store metadata for alerting
            meta.append((name, valid))

            tasks.append(
                loop.run_in_executor(
                    None,
                    self.anomaly_engine.analyze_series,
                    name,
                    values,
                    valid
                )
            )

        results = loop.run_until_complete(asyncio.gather(*tasks))

        threats = []

        for i, result in enumerate(results):
            if not result:
                continue

            threats.append(result)

            # ============================
            # 🚨 GLOBAL ALERT TRIGGER
            # ============================
            try:
                name, raw_events = meta[i]

                asyncio.run(GlobalAlertStore.push_alert({
                    "title": f"Anomaly detected in {name}",
                    "severity": result.get("severity", "HIGH"),
                    "attack_type": result.get("attack_type", "unknown"),
                    "summary": result.get("summary", "Suspicious activity detected"),
                    "source_events": len(raw_events)
                }))

            except Exception as e:
                logger.error(f"Alert push failed: {e}")

        logger.info(f"🚨 Detected {len(threats)} anomalies")

        return threats
    # =====================================================
    # MAIN CYCLE
    # =====================================================
    def run_cycle(self):
        logger.info("🔄 Starting collection cycle")

        events = asyncio.run(self.collect_events_async())

        logger.info(f"📊 Collected {len(events)} events")

        grouped = {
            "auth": [],
            "network": [],
            "security": [],
            "system": []
        }

        # ================================
        # FAST GROUPING 
        # ================================
        for e in events:
            if not isinstance(e, dict):
                grouped["system"].append(e)
                continue

            payload = e.get("event", {}) if isinstance(e.get("event"), dict) else {}
            normalized = {**e, **payload}

            src = str(normalized.get("source", "system")).lower()
            attack_type = str(normalized.get("attack_type", "")).lower()

            if "soc_sim" in src or attack_type:
                if "brute" in attack_type:
                    grouped["auth"].append(normalized)
                elif "ddos" in attack_type or "scan" in attack_type:
                    grouped["network"].append(normalized)
                elif "error" in attack_type:
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

        # ================================
        # PARALLEL ANOMALY ENGINE
        # ================================
        threats = self.run_anomaly_parallel(grouped)

        # ================================
        # INTELLIGENCE ENGINE (SYNC)
        # ================================
        reports = self.intel_engine.analyze(threats)

        logger.info(f"🧠 Generated {len(reports)} intelligence reports")

        return {
            "events": len(events),
            "threats": len(threats),
            "reports": len(reports)
        }

    # =====================================================
    # DAEMON LOOP
    # =====================================================
    def run(self):
        logger.info("🚀 SentinelAI Daemon Started")

        while True:
            try:
                start = time.time()

                result = self.run_cycle()

                logger.info(f"⏱️ Cycle completed in {time.time() - start:.2f}s")
                logger.info(f"📊 Summary: {result}")

            except Exception as e:
                logger.exception(f"Daemon error: {e}")

            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    SplunkDaemon().run()