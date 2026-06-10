from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid
from typing import List


class ThreatEvent(BaseModel):
    event_id: str = Field(
        default_factory=lambda: str(uuid.uuid4())[:8] # Shortened for clean dashboard indexing
    )
    source: str
    anomaly_type: str
    severity: str
    score: float 
    attack_type: str
    description: str
    
    
    recommendations: List[str] = Field(default_factory=list) 
    
    data_points: int
    acknowledged: bool = False
    investigated: bool = False
    
    # ✅ Updated default_factory to timezone-aware UTC to prevent deprecation warnings
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )