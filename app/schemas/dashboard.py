from pydantic import BaseModel


class MetricPoint(BaseModel):
    name: str
    count: int


class TimelinePoint(BaseModel):
    date: str
    count: int


class DashboardMetricsResponse(BaseModel):
    total_incidents: int
    open_incidents: int
    high_critical_incidents: int
    total_comments: int
    total_documents: int
    by_severity: list[MetricPoint]
    by_source: list[MetricPoint]
    timeline: list[TimelinePoint]
