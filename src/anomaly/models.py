from pydantic import BaseModel
from typing import  Optional

class ThreatFinding(BaseModel):
    source: str
    severity: str
    score: int
    anomaly_type: str
    description: str
    recommendation: str
    record_count: int