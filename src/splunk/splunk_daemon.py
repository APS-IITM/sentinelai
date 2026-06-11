"""
SentinelAI Background Daemon

Flow:
Splunk -> MCP Store -> Anomaly Engine -> Intelligence Engine
"""

import time
from loguru import logger

from src.mcp_tools.auth_tools import AuthTools
from src.mcp_tools.network_tools import NetworkTools
from src.mcp_tools.security_tools import SecurityTools
from src.mcp_tools.system_tools import SystemTools

from src.anomaly.analyzer import AnomalyAnalyzer
from src.intelligence.engine import IntelligenceEngine


POLL_INTERVAL = 60


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

        threats = self.anomaly_engine.analyze(events)

        logger.info(f"Detected {len(threats)} threats")

        reports = self.intel_engine.analyze(threats)

        logger.info(f"Generated {len(reports)} intelligence reports")

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