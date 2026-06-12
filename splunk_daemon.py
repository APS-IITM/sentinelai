import time
import asyncio
from loguru import logger

from src.mcp_tools.auth_tools import AuthTools
from src.mcp_tools.network_tools import NetworkTools
from src.mcp_tools.security_tools import SecurityTools
from src.mcp_tools.system_tools import SystemTools

from src.anomaly.analyzer import AnomalyAnalyzer
from src.intelligence.engine import IntelligenceEngine


POLL_INTERVAL = 10


class SplunkDaemon:

    def __init__(self):
        self.auth = AuthTools()
        self.network = NetworkTools()
        self.security = SecurityTools()
        self.system = SystemTools()

        self.anomaly_engine = AnomalyAnalyzer()
        self.intel_engine = IntelligenceEngine()

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

        threats = [r for r in results if r]

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