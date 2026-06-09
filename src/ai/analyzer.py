import json

from src.ai.client import model
from src.ai.prompts import SYSTEM_PROMPT

from src.storage.mcp_store import MCPStore
from src.storage.anomaly_store import AnomalyStore
from src.storage.ai_report_store import AIReportStore

from src.ai.model import AIReport


class AIAnalyzer:

    def __init__(self):
        pass

    # ======================================================
    # 📦 INTERNAL DATA LOADER
    # ======================================================
    def _load_data(self, source_type: str):

        if source_type == "anomaly":
            return AnomalyStore.get_all()

        if source_type == "all":
            return {
                "auth": MCPStore.get("auth"),
                "network": MCPStore.get("network"),
                "security": MCPStore.get("security"),
                "system": MCPStore.get("system"),
                "anomalies": AnomalyStore.get_all()
            }

        return MCPStore.get(source_type)

    # ======================================================
    # 📊 BATCH SOC REPORT GENERATION (UNCHANGED CORE LOGIC)
    # ======================================================
    def generate_report(self, source_type: str = "all"):

        telemetry = self._load_data(source_type)

        if not telemetry:
            return "No telemetry data available for analysis."

        highest_severity = "LOW"

        if source_type == "anomaly":

            severities = [
                item.get("severity", "LOW")
                for item in telemetry
            ]

            if "CRITICAL" in severities:
                highest_severity = "CRITICAL"
            elif "HIGH" in severities:
                highest_severity = "HIGH"
            elif "MEDIUM" in severities:
                highest_severity = "MEDIUM"

        prompt = f"""
{SYSTEM_PROMPT}

======================================================
SENTINELAI TELEMETRY ANALYSIS
======================================================

Data Source:
{source_type}

Event Count:
{len(telemetry)}

Highest Severity:
{highest_severity}

Telemetry Payload:
{json.dumps(telemetry, indent=2)}

Generate a complete SOC report.
"""

        try:
            response = model.generate_content(prompt)
            report_text = response.text

            report = AIReport(
                source_type=source_type,
                event_count=len(telemetry),
                highest_severity=highest_severity,
                summary=report_text[:500],
                generated_report=report_text
            )

            AIReportStore.save(report.model_dump(mode="json"))

            return report

        except Exception as e:
            raise RuntimeError(f"Gemini analysis failed: {e}")

    # ======================================================
    # ⚡ FIXED: REAL-TIME SINGLE EVENT ANALYSIS (MISSING BEFORE)
    # ======================================================
    def analyze_event(self, event):
        """
        FIX: This was missing and caused your crash.
        Used by:
        - Streamlit UI
        - Attack Simulator
        - Intelligence Engine
        """

        try:
            prompt = f"""
{SYSTEM_PROMPT}

======================================================
SINGLE EVENT FORENSIC ANALYSIS
======================================================

Source:
{getattr(event, 'source', 'UNKNOWN')}

Attack Type:
{getattr(event, 'attack_type', 'UNKNOWN')}

Severity:
{getattr(event, 'severity', 'LOW')}

Description:
{getattr(event, 'description', '')}

Data Points:
{getattr(event, 'data_points', 0)}

Generate a SOC forensic intelligence report for this event.
"""

            response = model.generate_content(prompt)
            report_text = response.text

            report = AIReport(
                source_type="single_event",
                event_count=1,
                highest_severity=getattr(event, "severity", "LOW"),
                summary=report_text[:500],
                generated_report=report_text
            )

            AIReportStore.save(report.model_dump(mode="json"))

            return report_text

        except Exception as e:
            raise RuntimeError(f"AI single-event analysis failed: {e}")