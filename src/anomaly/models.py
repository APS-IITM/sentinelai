from pydantic import BaseModel


class ThreatEvent(BaseModel):
    source: str
    anomaly_type: str
    severity: str
    score: int
    attack_type: str
    description: str
    recommendation: str
    data_points: int