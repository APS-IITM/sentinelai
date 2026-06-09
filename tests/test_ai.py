"""
SentinelAI - AI Layer Test
"""

from src.ai.analyzer import AIAnalyzer
from src.anomaly.models import ThreatEvent


def main():

    print("=" * 60)
    print(" SENTINELAI AI LAYER TEST ")
    print("=" * 60)

    event = ThreatEvent(
        source="NETWORK_TRAFFIC",
        anomaly_type="VOLUME_SPIKE",
        severity="HIGH",
        score=92,
        attack_type="DDOS_ATTACK",
        description="Network spike detected",
        recommendation="Investigate IPs",
        data_points=500
    )

    ai = AIAnalyzer()

    try:
        report = ai.analyze_event(event)
        print("\n🤖 AI REPORT:\n")
        print(report)

    except Exception as e:
        print(f"❌ AI Error: {e}")


if __name__ == "__main__":
    main()