from pydantic import BaseModel


class TriageRequest(BaseModel):
    text: str


class TriageResponse(BaseModel):
    severity: str
    summary: str
    recommendation: str
    threat_type: str
    provider: str
