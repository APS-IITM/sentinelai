from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class ThreatEvent(BaseModel):
    event_id: str = Field(
        default_factory=lambda: str(uuid.uuid4())
    )
    source: str
    anomaly_type: str
    severity: str
    score: int
    attack_type: str
    description: str
    recommendation: str
    data_points: int
    acknowledged: bool = False
    investigated: bool = False
    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )