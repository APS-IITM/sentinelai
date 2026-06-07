from src.ai.client import model
from src.ai.prompts import SYSTEM_PROMPT

class AIAnalyzer:

    def analyze_event(self, threat_event) -> str:
        """
        Ingests the multi-scenario manifest telemetry, formats the engineering prompt,
        and retrieves the raw markdown analysis payload from the Gemini API.
        """
        prompt = f"""
{SYSTEM_PROMPT}

Security Incident

Source:
{threat_event.source}

Anomaly Type:
{threat_event.anomaly_type}

Severity:
{threat_event.severity}

Score:
{threat_event.score}

Attack Type:
{threat_event.attack_type}

Description:
{threat_event.description}

Recommendation:
{threat_event.recommendation}

Data Points:
{threat_event.data_points}
"""

        # Call the Google Gemini API endpoint
        response = model.generate_content(prompt)
        
        # Return the clean text payload directly to the caller without printing anything here
        return response.text