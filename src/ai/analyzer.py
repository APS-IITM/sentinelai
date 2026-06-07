import os

from src.ai.client import client
from src.ai.prompts import SYSTEM_PROMPT


class AIAnalyzer:

    def __init__(self):

        self.model = os.getenv(
            "AI_MODEL",
            "gpt-4.1-mini"
        )

    def analyze_event(
        self,
        threat_event
    ):

        prompt = f"""
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

        response = (
            client.chat.completions.create(
                model=self.model,
                temperature=0.2,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
        )

        return (
            response
            .choices[0]
            .message.content
        )