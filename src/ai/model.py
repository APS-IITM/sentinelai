from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class AIReport(BaseModel):
    report_id: str = Field(
        default_factory=lambda: str(uuid.uuid4())
    )
    source_type: str
    event_count: int
    highest_severity: str
    summary: str
    generated_report: str
    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )