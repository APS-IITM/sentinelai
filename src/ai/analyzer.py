import json

from src.ai.client import model
from src.ai.prompts import SYSTEM_PROMPT

from src.ai.model import AIReport
from src.storage.ai_report_store import AIReportStore


class AIAnalyzer:

    # -----------------------------------------------------
    # BATCH / SOC REPORT GENERATION
    # -----------------------------------------------------
    def generate_report(self, telemetry: dict | list):

        if not telemetry:
            return None

        highest_severity = self._extract_severity(telemetry)

        prompt = f"""
{SYSTEM_PROMPT}

======================================================
SENTINELAI SOC ANALYSIS
======================================================

Telemetry:
{json.dumps(telemetry, indent=2)}

Severity Context:
{highest_severity}

Generate a SOC intelligence report including:
- attack summary
- root cause
- impact analysis
- mitigation strategy
"""

        try:
            response = model.generate_content(prompt)

            report = AIReport(
                source_type="soc_batch",
                event_count=self._count_events(telemetry),
                highest_severity=highest_severity,
                summary=response.text[:500],
                generated_report=response.text
            )

            # -------------------------------------------------
            # ✅ SAVE VIA AIReportStore (FIXED HERE)
            # -------------------------------------------------
            AIReportStore.save(report.model_dump(mode="json"))

            return report

        except Exception as e:
            raise RuntimeError(f"AI report generation failed: {e}")

    # -----------------------------------------------------
    # SINGLE EVENT FORENSIC ANALYSIS
    # -----------------------------------------------------
    def analyze_event(self, event):

        prompt = f"""
{SYSTEM_PROMPT}

======================================================
SINGLE EVENT FORENSIC ANALYSIS
======================================================

Source: {getattr(event, 'source', 'UNKNOWN')}
Attack Type: {getattr(event, 'attack_type', 'UNKNOWN')}
Severity: {getattr(event, 'severity', 'LOW')}
Description: {getattr(event, 'description', '')}
Data Points: {getattr(event, 'data_points', 0)}

Provide:
- root cause
- attack interpretation
- mitigation steps
"""

        try:
            response = model.generate_content(prompt)
            return response.text

        except Exception as e:
            raise RuntimeError(f"AI single-event analysis failed: {e}")

    # -----------------------------------------------------
    # HELPERS
    # -----------------------------------------------------
    def _extract_severity(self, telemetry):

        severities = []

        items = (
            telemetry if isinstance(telemetry, list)
            else telemetry.get("anomalies", [])
            if isinstance(telemetry, dict)
            else []
        )

        for item in items:
            if isinstance(item, dict):
                severities.append(item.get("severity", "LOW"))

        if "CRITICAL" in severities:
            return "CRITICAL"
        if "HIGH" in severities:
            return "HIGH"
        if "MEDIUM" in severities:
            return "MEDIUM"

        return "LOW"

    def _count_events(self, telemetry):

        if isinstance(telemetry, list):
            return len(telemetry)

        if isinstance(telemetry, dict):
            return sum(
                len(v) if isinstance(v, list) else 1
                for v in telemetry.values()
            )

        return 0