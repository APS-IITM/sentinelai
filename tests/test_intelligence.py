"""
SentinelAI - Intelligence Engine Test
"""

from src.anomaly.models import ThreatEvent
from src.intelligence.engine import IntelligenceEngine


def main():

    print("=" * 60)
    print(" SENTINELAI INTELLIGENCE ENGINE TEST ")
    print("=" * 60)

    events = [
        ThreatEvent(
            source="AUTH",
            anomaly_type="VOLUME_SPIKE",
            severity="HIGH",
            score=80,
            attack_type="BRUTE_FORCE_ATTACK",
            description="Login spike",
            recommendation="Lock accounts",
            data_points=300
        ),
        ThreatEvent(
            source="NETWORK",
            anomaly_type="VOLUME_SPIKE",
            severity="CRITICAL",
            score=95,
            attack_type="DDOS_ATTACK",
            description="Traffic spike",
            recommendation="Enable mitigation",
            data_points=1200
        )
    ]

    engine = IntelligenceEngine()
    report = engine.analyze(events)

    print("\n📊 INCIDENT TYPE:", report.incident_type)
    print("⚠️ SEVERITY:", report.severity)

    print("\n🧠 MITRE:")
    for m in report.mitre_techniques:
        print("-", m)

    print("\n📍 TIMELINE:")
    for t in report.timeline:
        print(t)

    print("\n💡 RECOMMENDATIONS:")
    for r in report.recommendations:
        print("-", r)


if __name__ == "__main__":
    main()