from src.ai.client import model
from src.ai.prompts import SYSTEM_PROMPT
from rich.console import Console
from rich.markdown import Markdown


console = Console()

class AIAnalyzer:

    def analyze_event(
        self,
        threat_event
    ):

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
        response = model.generate_content(
            prompt
        )

        raw_markdown = response.text

        # -------------------------------------------------------------
        # BEAUTIFUL TERMINAL RENDERING LAYER
        # -------------------------------------------------------------
        console.print("\n")
        console.print("[bold cyan]🤖 AI SOC ANALYST BRIEFING[/bold cyan]", justify="center")
        console.print("[dim]─" * console.width + "[/dim]")
        
        # Convert raw Markdown text string into structured console objects
        markdown_content = Markdown(raw_markdown)
        console.print(markdown_content)
        
        console.print("[dim]─" * console.width + "[/dim]\n")
        # -------------------------------------------------------------

        return raw_markdown
