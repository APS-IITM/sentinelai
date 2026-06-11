"""
SentinelAI Background Daemon - Fixed Version
Flow: Splunk -> MCP Store -> Anomaly Engine -> Intelligence Engine
"""

import time
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

    def collect_events(self):
        events = []

        try:
            events.extend(self.auth.get_auth_logs())
        except Exception as e:
            logger.error(f"Auth collection failed: {e}")

        try:
            events.extend(self.network.get_network_logs())
        except Exception as e:
            logger.error(f"Network collection failed: {e}")

        try:
            # FIX: Changed from get_auth_logs() to get_security_logs()
            # Verify the exact method name in your src/mcp_tools/security_tools.py file
            if hasattr(self.security, 'get_security_logs'):
                events.extend(self.security.get_security_logs())
            else:
                events.extend(self.security.get_auth_logs()) 
        except Exception as e:
            logger.error(f"Security collection failed: {e}")

        try:
            events.extend(self.system.get_system_logs())
        except Exception as e:
            logger.error(f"System collection failed: {e}")

        return events

    def run_cycle(self):
        logger.info("Starting collection cycle")
        events = self.collect_events()
        logger.info(f"Collected {len(events)} events")

        if not events:
            logger.warning("No events collected in this cycle.")
            return

        grouped = {
            "auth": [],
            "network": [],
            "security": [],
            "system": []
        }

        for e in events:
            # Defensive check: if event is a string, wrap it or parse it
            if not isinstance(e, dict):
                # If your attack logs are raw strings, we try to categorize via raw text search
                src_str = str(e).lower()
                if "auth" in src_str: grouped["auth"].append({"raw": e})
                elif "network" in src_str: grouped["network"].append({"raw": e})
                elif "security" in src_str: grouped["security"].append({"raw": e})
                else: grouped["system"].append({"raw": e})
                continue

            # If it's a properly formatted dict
            src = e.get("source", "").lower()
            
            if "auth" in src:
                grouped["auth"].append(e)
            elif "network" in src:
                grouped["network"].append(e)
            elif "security" in src:
                grouped["security"].append(e)
            else:
                # Fallback check: check other fields if 'source' isn't explicitly set
                event_str = str(e).lower()
                if "auth" in event_str: grouped["auth"].append(e)
                elif "network" in event_str: grouped["network"].append(e)
                elif "security" in event_str: grouped["security"].append(e)
                else: grouped["system"].append(e)

        threats = []
        for name, group in grouped.items():
            if not group:
                continue  # Skip running the engine for empty sets

            values = [
                int(x.get("count", 1))
                if isinstance(x, dict) else 1
                for x in group
            ]

            logger.debug(f"Analyzing {name} series with data: {values}")
            
            threat = self.anomaly_engine.analyze_series(
                name,
                values,
                group   
            )

            if threat:
                threats.append(threat)

        if threats:
            logger.warning(f"Detected {len(threats)} threats!")
            reports = self.intel_engine.analyze(threats)
            logger.info(f"Generated {len(reports)} intelligence reports")
        else:
            logger.info("No threats detected in this cycle.")

    def run(self):
        logger.info("SentinelAI Daemon Started")
        while True:
            try:
                self.run_cycle()
            except Exception as e:
                logger.exception(f"Daemon error: {e}")
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    SplunkDaemon().run()