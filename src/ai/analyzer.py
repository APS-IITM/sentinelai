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
            # ✅ SAVE VIA AIReportStore
            # -------------------------------------------------
            AIReportStore.save(report.model_dump(mode="json"))

            return report

        except Exception as e:
            raise RuntimeError(f"AI report generation failed: {e}")

    # -----------------------------------------------------
    # SINGLE EVENT FORENSIC ANALYSIS 
    # -----------------------------------------------------
    def analyze_event(self, event):

        source = getattr(event, 'source', 'UNKNOWN')
        attack_type = getattr(event, 'attack_type', 'UNKNOWN')
        severity = getattr(event, 'severity', 'LOW')
        description = getattr(event, 'description', '')
        data_points = getattr(event, 'data_points', 0)

        prompt = f"""
{SYSTEM_PROMPT}

======================================================
SINGLE EVENT FORENSIC ANALYSIS
======================================================

Source: {source}
Attack Type: {attack_type}
Severity: {severity}
Description: {description}
Data Points: {data_points}

Provide:
- root cause
- attack interpretation
- mitigation steps
"""

        try:
            response = model.generate_content(prompt)
            generated_text = response.text

            # -------------------------------------------------
            # ✅ FIX: BUILD AND SAVE REPORT TO SUPABASE
            # -------------------------------------------------
            report = AIReport(
                source_type=f"single_{str(source).lower()}",
                event_count=1,
                highest_severity=severity,
                summary=f"Forensic snapshot for {attack_type} vector on {source}.",
                generated_report=generated_text
            )
            
            # Save the record structure down to the cloud table mapping
            AIReportStore.save(report.model_dump(mode="json"))

            # Return the text string so threat_monitor.py can render it smoothly
            return generated_text

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