from pydantic import BaseModel, Field
from datetime import datetime

class ThreatEvent(BaseModel):
    source: str
    anomaly_type: str
    severity: str
    score: int
    attack_type: str
    description: str
    recommendation: str
    data_points: int
    timestamp: datetime = Field(default_factory=datetime.now)
