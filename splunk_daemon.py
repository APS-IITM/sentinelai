"""
SentinelAI Background Daemon

Flow:
Splunk -> MCP Store -> Anomaly Engine -> Intelligence Engine
"""

import time
import os
import json
from loguru import logger

from src.mcp_tools.auth_tools import AuthTools
from src.mcp_tools.network_tools import NetworkTools
from src.mcp_tools.security_tools import SecurityTools
from src.mcp_tools.system_tools import SystemTools

from src.anomaly.analyzer import AnomalyAnalyzer
from src.intelligence.engine import IntelligenceEngine

POLL_INTERVAL = 10
SIMULATOR_LOG_PATH = "attack_stream.log"


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

        # 1. NATIVE MCP TOOL COLLECTION PIPELINE
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

        # 2. SIMULATOR STREAM INTERCEPTOR PIPELINE
        # Reads file-based streams written by the UI frontend
        if os.path.exists(SIMULATOR_LOG_PATH):
            try:
                with open(SIMULATOR_LOG_PATH, "r+", encoding="utf-8") as f:
                    lines = f.readlines()
                    for line in lines:
                        if not line.strip():
                            continue
                        try:
                            parsed_event = json.loads(line)
                            events.append(parsed_event)
                        except json.JSONDecodeError:
                            continue
                    
                    # Truncate/wipe log file immediately after successful ingest 
                    # to prevent duplicate anomaly triggers on subsequent cycles
                    f.seek(0)
                    f.truncate()
                logger.info(f"Ingested simulated attack vector records from {SIMULATOR_LOG_PATH}")
            except Exception as e:
                logger.error(f"Error extracting simulation log stream: {e}")

        return events

    def run_cycle(self):
        logger.info("Starting collection cycle")
        events = self.collect_events()
        logger.info(f"Collected {len(events)} total raw events")

        grouped = {
            "auth": [],
            "network": [],
            "security": [],
            "system": []
        }

        # DYNAMIC ROUTING & SIMULATOR ENGINE STYLE ALIGNMENT
        for e in events:
            if not isinstance(e, dict):
                grouped["system"].append(e)
                continue

            # Extract identifier parameters
            src = str(e.get("source", "system")).lower()
            attack_type = str(e.get("attack_type", "")).lower()

            # Cross-compatibility optimization check for your UI Simulator framework
            if "soc_sim" in src or attack_type != "":
                # Convert simulated envelope structure seamlessly to match Engine Style classifications
                if "brute" in attack_type:
                    grouped["auth"].append(e)
                elif "ddos" in attack_type or "scan" in attack_type:
                    grouped["network"].append(e)
                elif "error" in attack_type or "storm" in attack_type:
                    grouped["system"].append(e)
                else:
                    grouped["security"].append(e)
            else:
                # Standard native routing configuration for fallback loops
                if "auth" in src:
                    grouped["auth"].append(e)
                elif "network" in src:
                    grouped["network"].append(e)
                elif "security" in src:
                    grouped["security"].append(e)
                else:
                    grouped["system"].append(e)

        threats = []

        # PREPARATION AND ANOMALY EVALUATION ENGINE INTERACTION
        for name, group in grouped.items():
            # Standard metric array extraction
            values = [
                int(x.get("count", 1)) if isinstance(x, dict) else 1
                for x in group
            ]

            # Fire analysis profile engine evaluation mapping
            threat = self.anomaly_engine.analyze_series(
                name,
                values,
                group   
            )

            if threat:
                threats.append(threat)

        logger.info(f"Detected {len(threats)} threats across telemetry streams")

        # GENERATING UPSTREAM SECURITY REPORT INTELLIGENCE
        reports = self.intel_engine.analyze(threats)
        logger.info(f"Generated {len(reports)} intelligence reports")

    def run(self):
        logger.info("SentinelAI Daemon Started")
        while True:
            try:
                self.run_cycle()
            except Exception as e:
                logger.exception(f"Daemon runtime anomaly error: {e}")

            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    SplunkDaemon().run()