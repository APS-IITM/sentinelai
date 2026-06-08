"""
SentinelAI: State-Aware Forensic AI Reasoning Layer
Stages structural scenario metrics and executes a single consolidated Google Gemini API 
payload call on-demand when explicitly requested by a user or UI event.
"""

import json
from src.ai.client import model
from src.ai.prompts import SYSTEM_PROMPT

class AIAnalyzer:
    def __init__(self):
        # Internal temporary buffer to collect staged incident payloads
        self._staged_events = []

    def stage_event(self, threat_event) -> int:
        """
        Ingests and caches a ThreatEvent object without triggering the LLM API.
        Returns the current count of staged events in the queue.
        """
        self._staged_events.append(threat_event)
        return len(self._staged_events)

    def clear_buffer(self):
        """Resets the internal telemetry staging cache."""
        self._staged_events = []

    def has_staged_data(self) -> bool:
        """Helper to check if there is data waiting to be analyzed."""
        return len(self._staged_events) > 0

    def generate_report(self) -> str:
        """
        Compiles all staged logs into a comprehensive tactical prompt and 
        dispatches it to Google Gemini exactly ONCE. Clears buffer post-execution.
        """
        if not self._staged_events:
            return "### ⚪ AI Engine Report Warning\nNo incident telemetry has been staged for processing."

        # Compile and aggregate metadata parameters cleanly from all cached anomalies
        aggregated_incidents_payload = []
        highest_severity = "LOW"
        max_score = 0.0

        for idx, event in enumerate(self._staged_events, 1):
            # Extract underlying data configurations safely
            aggregated_incidents_payload.append({
                "incident_index": idx,
                "source": getattr(event, "source", "Unknown Subsystem"),
                "anomaly_type": getattr(event, "anomaly_type", "N/A"),
                "attack_type": getattr(event, "attack_type", "UNDETERMINED"),
                "score": getattr(event, "score", 0.0),
                "description": getattr(event, "description", "")
            })
            
            # Simple metadata resolution tracking
            current_score = getattr(event, "score", 0.0)
            if current_score > max_score:
                max_score = current_score
                highest_severity = getattr(event, "severity", "HIGH")

        # Construct the unified system macro prompt blueprint
        prompt = f"""
{SYSTEM_PROMPT}

========================================================================
🚨 MULTI-VECTOR SECURITY INCIDENT BATCH REPORT FOR EVALUATION
========================================================================
Global Peak Severity: {highest_severity}
Global Maximum Threat Score: {max_score}
Total Aggregated Telemetry Vectors Staged: {len(self._staged_events)}

------------------------------------------------------------------------
📊 INGESTED FORENSIC PAYLOAD MANIFEST
------------------------------------------------------------------------
{json.dumps(aggregated_incidents_payload, indent=2)}

------------------------------------------------------------------------
📝 SYSTEM INSTRUCTION
------------------------------------------------------------------------
Analyze the structured architectural payload sequence above. Correlate the 
interleaved timeline vectors, assess environmental blast-radius impact limits, 
and execute a comprehensive forensic executive summary report complete with 
actionable containment playbook recommendations.
"""

        try:
            # Dispatch the single macro context query directly to Gemini
            response = model.generate_content(prompt)
            report_output = response.text
            
            # Flush the memory storage buffer post-generation to prevent duplicate correlation bleeding
            self.clear_buffer()
            return report_output
            
        except Exception as e:
            return f"### 🔴 AI Core Exception\nAn error occurred while generating the report via the Gemini engine endpoint: `{str(e)}`"