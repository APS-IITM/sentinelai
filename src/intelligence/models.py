from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid
from typing import List, Dict

class IntelligenceReport(BaseModel):
    report_id: str = Field(
        default_factory=lambda: str(uuid.uuid4())[:8] # Shortened for dashboard visual consistency
    )
    incident_type: str
    severity: str
    attack_story: str
    
    timeline: List[Dict] = Field(default_factory=list)
    mitre_techniques: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    
    event_count: int
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc) 
    )