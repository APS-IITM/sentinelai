from src.anomaly.models import ThreatEvent
from src.intelligence.engine import IntelligenceEngine


def create_test_events():
    return [

        ThreatEvent(
            source="Authentication Logs",
            anomaly_type="VOLUME_SPIKE",
            severity="HIGH",
            score=82,
            attack_type="BRUTE_FORCE_ATTACK",
            description="Multiple failed login attempts detected",
            recommendation="Lock suspicious accounts",
            data_points=350
        ),

        ThreatEvent(
            source="Network Logs",
            anomaly_type="VOLUME_SPIKE",
            severity="MEDIUM",
            score=65,
            attack_type="NETWORK_SCAN",
            description="Large number of ports scanned",
            recommendation="Block source IP",
            data_points=220
        ),

        ThreatEvent(
            source="System Logs",
            anomaly_type="VOLUME_SPIKE",
            severity="CRITICAL",
            score=95,
            attack_type="DDOS_ATTACK",
            description="Traffic spike detected",
            recommendation="Enable rate limiting",
            data_points=1200
        )
    ]


def main():

    print("\n" + "=" * 60)
    print(" SENTINELAI DAY INTELLIGENCE ENGINE TEST ")
    print("=" * 60)

    events = create_test_events()

    print(f"\nLoaded {len(events)} threat events")

    engine = IntelligenceEngine()

    report = engine.analyze(events)

    if not report:
        print("No intelligence report generated")
        return

    print("\n" + "=" * 60)
    print(" INCIDENT TYPE ")
    print("=" * 60)

    print(report.incident_type)

    print("\n" + "=" * 60)
    print(" SEVERITY ")
    print("=" * 60)

    print(report.severity)

    print("\n" + "=" * 60)
    print(" ATTACK STORY ")
    print("=" * 60)

    print(report.attack_story)

    print("\n" + "=" * 60)
    print(" MITRE TECHNIQUES ")
    print("=" * 60)

    for technique in report.mitre_techniques:
        print(f"• {technique}")

    print("\n" + "=" * 60)
    print(" TIMELINE ")
    print("=" * 60)

    for item in report.timeline:
        print(item)

    print("\n" + "=" * 60)
    print(" RECOMMENDATIONS ")
    print("=" * 60)

    for rec in report.recommendations:
        print(f"• {rec}")

    print("\n" + "=" * 60)
    print(" FULL JSON REPORT ")
    print("=" * 60)

    print(
        report.model_dump_json(
            indent=4
        )
    )


if __name__ == "__main__":
    main()