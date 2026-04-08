from collections import Counter, defaultdict
from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.models.document import Document
from app.models.incident import Incident


def build_dashboard_metrics(db: Session) -> dict:
    incidents = db.query(Incident).all()
    total_comments = db.query(Comment).count()
    total_documents = db.query(Document).count()

    severity_counter = Counter(i.severity for i in incidents)
    source_counter = Counter(i.source for i in incidents)

    timeline_counter = defaultdict(int)
    for incident in incidents:
        date_key = incident.created_at.strftime("%Y-%m-%d")
        timeline_counter[date_key] += 1

    return {
        "total_incidents": len(incidents),
        "open_incidents": sum(1 for i in incidents if i.status.lower() == "open"),
        "high_critical_incidents": sum(1 for i in incidents if i.severity in {"High", "Critical"}),
        "total_comments": total_comments,
        "total_documents": total_documents,
        "by_severity": [{"name": k, "count": v} for k, v in severity_counter.items()],
        "by_source": [{"name": k, "count": v} for k, v in source_counter.items()],
        "timeline": [{"date": k, "count": v} for k, v in sorted(timeline_counter.items())],
    }
