from src.ai.analyzer import AIAnalyzer

from src.anomaly.models import (
    ThreatEvent
)

event = ThreatEvent(
    source="NETWORK_TRAFFIC",
    anomaly_type="VOLUME_SPIKE",
    severity="HIGH",
    score=87,
    attack_type="DDOS_ATTACK",
    description="Traffic spike detected",
    recommendation="Investigate",
    data_points=450
)

ai = AIAnalyzer()

report = ai.analyze_event(
    event
)

print(report)