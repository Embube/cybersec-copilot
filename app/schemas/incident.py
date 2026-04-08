from datetime import datetime

from pydantic import BaseModel


class IncidentCreate(BaseModel):
    title: str
    source: str = "Manual"
    severity: str = "Medium"
    threat_type: str = "Unknown"
    summary: str
    analyst_notes: str | None = None
    raw_event: str | None = None
    status: str = "Open"


class IncidentUpdate(BaseModel):
    title: str | None = None
    source: str | None = None
    severity: str | None = None
    threat_type: str | None = None
    summary: str | None = None
    analyst_notes: str | None = None
    raw_event: str | None = None
    status: str | None = None


class IncidentResponse(BaseModel):
    id: int
    title: str
    source: str
    severity: str
    threat_type: str
    summary: str
    analyst_notes: str | None = None
    raw_event: str | None = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    incident_id: int
    body: str


class CommentResponse(BaseModel):
    id: int
    incident_id: int
    author: str
    body: str
    created_at: datetime

    class Config:
        from_attributes = True
