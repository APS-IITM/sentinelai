from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class IntelligenceReport(BaseModel):

    report_id: str = Field(
        default_factory=lambda: str(uuid.uuid4())
    )

    incident_type: str

    severity: str

    attack_story: str

    timeline: list

    mitre_techniques: list

    recommendations: list

    event_count: int

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )