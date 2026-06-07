from pydantic import BaseModel


class IntelligenceReport(BaseModel):

    incident_type: str

    severity: str

    attack_story: str

    timeline: list

    mitre_techniques: list

    recommendations: list