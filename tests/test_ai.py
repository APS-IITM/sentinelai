from src.ai.analyzer import AIAnalyzer

from src.anomaly.models import (
    ThreatEvent
)

event = ThreatEvent(
    source="NETWORK_TRAFFIC",
    anomaly_type="VOLUME_SPIKE",
    severity="HIGH",
    score=92,
    attack_type="DDOS_ATTACK",
    description="Sudden spike in network traffic detected",
    recommendation="Investigate source IPs",
    data_points=500
)

ai = AIAnalyzer()

report = ai.analyze_event(
    event
)

print(report)