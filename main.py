
"""
SentinelAI: Autonomous Incident Intelligence Engine (Core Backend CLI Orchestrator)
Handles data routing between Splunk MCP tools, hybrid mathematical anomaly execution,
cross-domain incident correlation, and the generative AI reasoning layer.
"""

import os
import sys
import logging
import time
from datetime import datetime

# ==========================================
# 📊 ARCHITECTURAL BACKBONE: ENGINE IMPORTS
# ==========================================
from src.mcp_tools.auth_tools import AuthTools
from src.mcp_tools.security_tools import SecurityTools
from src.mcp_tools.system_tools import SystemTools
from src.mcp_tools.network_tools import NetworkTools

from src.anomaly.analyzer import AnomalyAnalyzer
from src.intelligence.engine import IntelligenceEngine
from src.utils.formatter import pretty_json

# Configure structured industry-standard enterprise logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("SentinelAI-Core")

# ==========================================
# 🤖 ADVANCED INTELLIGENCE / LLM LAYER
# ==========================================
try:
    from src.ai.analyzer import AIAnalyzer
    ai_enabled = True
    logger.info("AI Reasoning Engine successfully integrated.")
except Exception as e:
    ai_enabled = False
    AIAnalyzer = None
    logger.warning(f"AI Analyzer disabled (Module import skipped/unavailable): {e}")


# ==========================================
# 🧰 RAW TEXT FORMATTING UTILITY LAYER
# ==========================================
class BackendConsoleFormatter:
    """Provides high-scannability terminal dividers without frontend engine dependencies."""
    WIDTH = 80

    @classmethod
    def print_header(cls, title: str):
        print("\n" + "=" * cls.WIDTH)
        print(f" [ENGINE] {title.upper()} ".center(cls.WIDTH, "="))
        print("=" * cls.WIDTH)

    @classmethod
    def print_section(cls, title: str, response: dict):
        print("\n" + "─" * cls.WIDTH)
        print(f" ▸ TELEMETRY SOURCE: {title.upper()} ".center(cls.WIDTH, "─"))
        print("─" * cls.WIDTH)
        print(f"   Status:    {'🟢 SUCCESS' if response.get('success') else '🔴 FAILED'}")
        print(f"   Records:   {response.get('count', 0)}")
        
        if response.get("error"):
            print(f"   Error Log: {response['error']}")
            return
            
        data = response.get("data", [])
        if data:
            print("   Sample Data Event Payload:")
            print(pretty_json(data[0] if isinstance(data, list) and len(data) > 0 else data))


# ==========================================
# 🧬 TIME-SERIES NUMERICAL EXTRACTOR
# ==========================================
def extract_counts(response: dict) -> list:
    """Safely extracts raw time-series metrics from Splunk responses for mathematical analysis."""
    if not response or not isinstance(response, dict):
        return []
    
    data = response.get("data", [])
    return [int(item["count"]) for item in data if "count" in item and str(item["count"]).isdigit()]


# ==========================================
# 🚀 THE UNIFIED INTELLIGENCE PIPELINE
# ==========================================
def run_pipeline(anomaly_engine, intelligence_engine, ai_engine, active_threats: list):
    """
    Executes core pipeline lifecycle routing:
    Anomaly Vector Processing ➔ Intelligence Engine Correlation ➔ LLM Forensic Report Execution
    """
    BackendConsoleFormatter.print_header("Unified Incident Correlation & Triage")
    
    if not active_threats:
        logger.info("Operational status normal. No anomalies identified across active log scopes.")
        return

    # 1. Coordinate Threat Arrays inside the CTI Intelligence Engine
    logger.info(f"Passing {len(active_threats)} flagged mathematical anomalies into correlation engine...")
    start_time = time.time()
    cti_report = intelligence_engine.analyze(active_threats)
    execution_lag = (time.time() - start_time) * 1000

    if not cti_report:
        logger.error("Threat correlation engine failed to generate an incident overview matrix.")
        return

    # Print out pure structured metrics data fields
    print(f"\n🔥 [MUTLI-STAGE SECURITY INCIDENT CORRELATED]")
    print(f"  ├── Signature Campaign Classification : {cti_report.incident_type}")
    print(f"  ├── Peak Integrated Severity Context  : {cti_report.severity}")
    print(f"  └── Core Engine Processing Latency   : {execution_lag:.2f} ms")

    print(f"\n🎯 MITRE ATT&CK Mapping Profiles:")
    for technique in cti_report.mitre_techniques:
        print(f"  [+] Technique ID/Name: {technique}")

    print(f"\n⏱️  Chronological Incident Lifecycle Audit Trail:")
    for idx, step in enumerate(cti_report.timeline, 1):
        print(f"  ({idx}) {step.get('time')} | Target: {step.get('source')} | Attack Phase: {step.get('attack')} [{step.get('severity')}]")

    # 2. Handoff to Generative AI Forensic Reasoning Layer
    if ai_enabled and ai_engine:
        BackendConsoleFormatter.print_header("Generative AI Forensic Security Briefing")
        logger.info("Routing structured incident payload to Google Gemini Core API...")
        
        try:
            # Anchor prompt to primary anomaly signature
            primary_threat = active_threats[0]
            primary_threat.description = (
                f"Multi-stage campaign correlated as {cti_report.incident_type}. "
                f"Forensic lifecycle path summary: {cti_report.attack_story}"
            )
            primary_threat.severity = cti_report.severity

            # Fire API call and dump pure raw text markdown output to CLI
            ai_briefing = ai_engine.analyze_event(primary_threat)
            print(ai_briefing)
            
        except Exception as e:
            logger.error(f"Generative AI security briefing layer exception: {e}")


# ==========================================
# 🏁 MAIN ENGINE SYSTEM EXECUTION
# ==========================================
def main():
    BackendConsoleFormatter.print_header("SentinelAI System Initialization Sequence")
    
    # Instantiate Toolsets
    auth_tool = AuthTools()
    security_tool = SecurityTools()
    system_tool = SystemTools()
    network_tool = NetworkTools()

    # Instantiate Analytical Core Pipelines
    anomaly_engine = AnomalyAnalyzer()
    intelligence_engine = IntelligenceEngine()
    ai_engine = AIAnalyzer() if ai_enabled else None

    logger.info("Querying Splunk indices via parallel Model Context Protocol tools...")
    splunk_live = True
    
    try:
        auth_logs = auth_tool.get_auth_logs(limit=20)
        error_logs = security_tool.get_error_logs(limit=20)
        system_logs = system_tool.get_system_logs(limit=20)
        network_logs = network_tool.get_network_logs(limit=20)
        search_logs = system_tool.search_logs("login", limit=10)

        # Pull metric arrays for statistical analysis
        login_trend = system_tool.login_trend()
        error_trend = system_tool.error_trend()
        network_trend = network_tool.network_trend()
        
        if not isinstance(login_trend, dict) or "data" not in login_trend:
            splunk_live = False
    except Exception as e:
        logger.warning(f"Local Splunk operational pipeline unreachable/offline: {e}")
        splunk_live = False

    # ── HIGH-FIDELITY DEFENSIVE HACKATHON FALLBACK SYSTEM ──
    if not splunk_live:
        logger.info("💡 [MOCK ACTIVATED] Pre-populating deep operational logs to guarantee demo reliability:")
        
        auth_logs = {"success": True, "count": 1, "data": [{"user": "root", "host": "SRV-PROD-01", "status": "failed", "count": 240}]}
        error_logs = {"success": True, "count": 1, "data": [{"host": "APP-NODE-4", "source": "syslog", "count": 185}]}
        system_logs = {"success": True, "count": 1, "data": [{"sourcetype": "linux_secure", "count": 4120}]}
        network_logs = {"success": True, "count": 1, "data": [{"SRC": "192.168.1.50", "DST": "10.0.0.5", "PORT": "22", "ACTION": "DENY", "count": 1200}]}
        search_logs = {"success": True, "count": 1, "data": [{"host": "SRV-PROD-01", "sourcetype": "auth_logs", "count": 15}]}

        # Active Multi-Stage Attack Sequence Data (Port Scan ➔ Brute Force ➔ DDoS)
        login_trend = {"success": True, "data": [{"count": c} for c in [12, 14, 15, 11, 13, 12, 14, 16, 12, 15, 11, 14, 280]]}
        error_trend = {"success": True, "data": [{"count": c} for c in [2, 1, 3, 2, 4, 1, 2, 3, 1, 2, 4, 3, 195]]}
        network_trend = {"success": True, "data": [{"count": c} for c in [45, 52, 48, 50, 47, 53, 49, 51, 46, 50, 52, 48, 1420]]}

    # Print raw logs out to console
    BackendConsoleFormatter.print_section("Authentication Logs Subsystem", auth_logs)
    BackendConsoleFormatter.print_section("System Error Logs Subsystem", error_logs)
    BackendConsoleFormatter.print_section("System Core Topology Subsystem", system_logs)
    BackendConsoleFormatter.print_section("Network Boundary Ingress Subsystem", network_logs)
    BackendConsoleFormatter.print_section("Keyword Search Log Tracker Subsystem", search_logs)

    # Convert dictionary metrics into mathematical list arrays
    login_series = extract_counts(login_trend)
    error_series = extract_counts(error_trend)
    network_series = extract_counts(network_trend)

    BackendConsoleFormatter.print_header("Extracted Numerical Time-Series Signals")
    print(f" ▸ Auth Login Stream Count Vector  : {login_series}")
    print(f" ▸ System Error Stream Count Vector: {error_series}")
    print(f" ▸ Network Ingress Stream Count Vector: {network_series}")

    
    # ── RUN MATHEMATICAL ANOMALY ENGINE DETECTORS ──
    active_threat_profiles = []

    if login_series:
        threat = anomaly_engine.analyze_series("Authentication Logs", login_series)
        if threat: 
                active_threat_profiles.append(threat)

    if error_series:
        threat = anomaly_engine.analyze_series("System Error Logs", error_series)
        if threat: 
            active_threat_profiles.append(threat)

    if network_series:
        threat = anomaly_engine.analyze_series("Network Perimeter Logs", network_series)
        if threat: 
            active_threat_profiles.append(threat)

    # ── RUN ENTIRE PIPELINE END-TO-END ──
    run_pipeline(anomaly_engine, intelligence_engine, ai_engine, active_threat_profiles)

        # ── PERIMETER DEEP INFRASTRUCTURE METRIC CHECKS ──
    BackendConsoleFormatter.print_header("Active Perimeter Infrastructure Footprint Sweeps")
        
    if not splunk_live:
        failed_connections = {"success": True, "count": 1, "data": [{"SRC": "192.168.1.50", "DST": "10.0.0.5", "PORT": "22", "count": 940}]}
        top_sources = {"success": True, "count": 1, "data": [{"SRC": "192.168.1.50", "count": 45100}]}
        top_destinations = {"success": True, "count": 1, "data": [{"DST": "10.0.0.5", "count": 82100}]}
        port_scan = {"success": True, "count": 1, "data": [{"SRC": "192.168.1.50", "unique_ports": 412}]}
    else:
        failed_connections = network_tool.failed_connections()
        top_sources = network_tool.top_source_ips()
        top_destinations = network_tool.top_destination_ips()
        port_scan = network_tool.port_scan_detection()

    BackendConsoleFormatter.print_section("Perimeter Connection Drops (ACTION=DENY)", failed_connections)
    BackendConsoleFormatter.print_section("Primary Volumetric Source Connection IPs", top_sources)
    BackendConsoleFormatter.print_section("Primary Volumetric Destination Connection IPs", top_destinations)
    BackendConsoleFormatter.print_section("Infrastructure Port-Scan Recon Signatures", port_scan)


if __name__ == "__main__":
    start_runtime = time.time()
    main()
    logger.info(f"Total Triage Process Finished in {(time.time() - start_runtime):.4f} seconds.")
