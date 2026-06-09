"""
SentinelAI: Autonomous Incident Intelligence Engine (Core Backend CLI Orchestrator)
Handles:
- Splunk MCP ingestion
- Anomaly detection engine
- Cross-domain intelligence correlation
- MITRE mapping
- Generative AI forensic analysis
- Persistent SOC-grade logging & audit trails
"""

import sys
import logging
import time
import uuid
import json
from datetime import datetime
from pathlib import Path

# ==========================================
# 📊 ARCHITECTURAL IMPORTS
# ==========================================
from src.mcp_tools.auth_tools import AuthTools
from src.mcp_tools.security_tools import SecurityTools
from src.mcp_tools.system_tools import SystemTools
from src.mcp_tools.network_tools import NetworkTools

from src.anomaly.analyzer import AnomalyAnalyzer
from src.intelligence.engine import IntelligenceEngine
from src.utils.formatter import pretty_json

# ==========================================
# 💾 PIPELINE PERSISTENCE LAYER
# ==========================================
PIPELINE_LOG = Path("data/pipeline_runs.json")
PIPELINE_LOG.parent.mkdir(parents=True, exist_ok=True)

def save_pipeline_run(payload: dict):
    existing = []

    if PIPELINE_LOG.exists():
        try:
            with open(PIPELINE_LOG, "r") as f:
                existing = json.load(f)
        except Exception:
            existing = []

    existing.append(payload)

    with open(PIPELINE_LOG, "w") as f:
        json.dump(existing, f, indent=2, default=str)


# ==========================================
# 📜 LOGGING CONFIG
# ==========================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("SentinelAI-Core")


# ==========================================
# 🤖 AI LAYER (OPTIONAL)
# ==========================================
try:
    from src.ai.analyzer import AIAnalyzer
    ai_enabled = True
    logger.info("AI Reasoning Engine loaded successfully.")
except Exception as e:
    AIAnalyzer = None
    ai_enabled = False
    logger.warning(f"AI Engine disabled: {e}")


# ==========================================
# 🧰 CLI FORMATTER
# ==========================================
class BackendConsoleFormatter:

    WIDTH = 80

    @classmethod
    def header(cls, title):
        print("\n" + "=" * cls.WIDTH)
        print(f" [ SENTINELAI ] {title} ".center(cls.WIDTH, "="))
        print("=" * cls.WIDTH)

    @classmethod
    def section(cls, title, data):
        print("\n" + "-" * cls.WIDTH)
        print(f" {title} ".center(cls.WIDTH, "-"))
        print("-" * cls.WIDTH)
        print(pretty_json(data))


# ==========================================
# 📊 TIME SERIES EXTRACTION
# ==========================================
def extract_counts(response: dict):
    if not response or not isinstance(response, dict):
        return []

    data = response.get("data", [])
    return [
        int(item["count"])
        for item in data
        if isinstance(item, dict) and str(item.get("count", "")).isdigit()
    ]


# ==========================================
# 🚀 PIPELINE EXECUTOR
# ==========================================
def run_pipeline(anomaly_engine, intelligence_engine, ai_engine, active_threats, pipeline_id, verbose=True):

    if verbose:
        BackendConsoleFormatter.header("INTELLIGENCE CORRELATION PIPELINE")

    if not active_threats:
        logger.info("No anomalies detected.")
        return None, None

    logger.info(f"[{pipeline_id}] Correlating {len(active_threats)} threats")

    start = time.time()
    cti_report = intelligence_engine.analyze(active_threats)
    latency = (time.time() - start) * 1000

    if not cti_report:
        logger.error("CTI generation failed")
        return None, None

    if verbose:
        print(f"\n🔥 INCIDENT TYPE: {cti_report.incident_type}")
        print(f"⚠️ SEVERITY: {cti_report.severity}")
        print(f"⏱️ LATENCY: {latency:.2f} ms")

        print("\nMITRE ATT&CK:")
        for m in cti_report.mitre_techniques:
            print(f" - {m}")

        print("\nTIMELINE:")
        for i, t in enumerate(cti_report.timeline, 1):
            print(f"{i}. {t['time']} | {t['source']} | {t['attack']} [{t['severity']}]")

    ai_output = None

    if ai_enabled and ai_engine:
        try:
            BackendConsoleFormatter.header("AI FORENSIC ANALYSIS")

            ai_output = ai_engine.analyze_batch(
                active_threats,
                cti_report
            )

            if verbose:
                print(ai_output)

        except Exception as e:
            logger.error(f"AI engine error: {e}")

    # SAVE PIPELINE EXECUTION
    save_pipeline_run({
        "pipeline_id": pipeline_id,
        "timestamp": datetime.utcnow().isoformat(),
        "threat_count": len(active_threats),
        "incident_type": cti_report.incident_type,
        "severity": cti_report.severity,
        "ai_enabled": ai_enabled
    })

    return cti_report, ai_output


# ==========================================
# 🚀 MAIN ORCHESTRATION PIPELINE
# ==========================================
def run_autonomous_triage(verbose=False):

    pipeline_id = str(uuid.uuid4())

    if verbose:
        BackendConsoleFormatter.header(f"PIPELINE START | ID: {pipeline_id}")

    # INIT TOOLS
    auth = AuthTools()
    security = SecurityTools()
    system = SystemTools()
    network = NetworkTools()

    anomaly_engine = AnomalyAnalyzer()
    intelligence_engine = IntelligenceEngine()
    ai_engine = AIAnalyzer() if ai_enabled else None

    logger.info(f"[{pipeline_id}] Fetching Splunk MCP data...")

    splunk_live = True

    try:
        auth_logs = auth.get_auth_logs(20)
        error_logs = security.get_error_logs(20)
        system_logs = system.get_system_logs(20)
        network_logs = network.get_network_logs(20)

        login_trend = system.login_trend()
        error_trend = system.error_trend()
        network_trend = network.network_trend()

    except Exception as e:
        logger.error(f"Splunk failure: {e}")
        splunk_live = False

    # MOCK FALLBACK
    if not splunk_live:

        logger.warning("Using MOCK dataset")

        auth_logs = {"data": [{"count": 240}]}
        error_logs = {"data": [{"count": 185}]}
        system_logs = {"data": [{"count": 4120}]}
        network_logs = {"data": [{"count": 1200}]}

        login_trend = {"data": [{"count": c} for c in [12, 14, 15, 280]]}
        error_trend = {"data": [{"count": c} for c in [2, 3, 195]]}
        network_trend = {"data": [{"count": c} for c in [50, 48, 1420]]}

    # EXTRACT SERIES
    login_series = extract_counts(login_trend)
    error_series = extract_counts(error_trend)
    network_series = extract_counts(network_trend)

    # ANOMALY DETECTION
    threats = []

    for name, series in [
        ("Auth Logs", login_series),
        ("Error Logs", error_series),
        ("Network Logs", network_series)
    ]:
        if series:
            t = anomaly_engine.analyze_series(name, series)
            if t:
                threats.append(t)

    # INTELLIGENCE PIPELINE
    cti, ai = run_pipeline(
        anomaly_engine,
        intelligence_engine,
        ai_engine,
        threats,
        pipeline_id,
        verbose
    )

    # FINAL OUTPUT
    return {
        "pipeline_id": pipeline_id,
        "threats": threats,
        "cti_report": cti,
        "ai_report": ai
    }


# ==========================================
# 🏁 CLI ENTRYPOINT
# ==========================================
if __name__ == "__main__":

    start = time.time()

    result = run_autonomous_triage(verbose=True)

    logger.info(
        f"Pipeline {result['pipeline_id']} completed in {(time.time() - start):.2f}s"
    )