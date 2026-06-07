from pydantic import BaseModel


class AIReport(BaseModel):

    summary: str

    root_cause: str

    impact: str

    recommendations: list[str]