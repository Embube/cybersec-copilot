from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.comment import Comment
from app.models.incident import Incident
from app.models.user import User
from app.schemas.incident import CommentCreate, CommentResponse, IncidentCreate, IncidentResponse, IncidentUpdate

router = APIRouter(tags=["incidents"])


@router.get("/", response_model=list[IncidentResponse])
def list_incidents(
    severity: str | None = Query(default=None),
    source: str | None = Query(default=None),
    keyword: str | None = Query(default=None),
    status: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Incident)
    if severity:
        query = query.filter(Incident.severity == severity)
    if source:
        query = query.filter(Incident.source == source)
    if status:
        query = query.filter(Incident.status == status)
    if keyword:
        like = f"%{keyword}%"
        query = query.filter(or_(Incident.title.ilike(like), Incident.summary.ilike(like), Incident.threat_type.ilike(like)))
    return query.order_by(Incident.created_at.desc()).all()


@router.post("/", response_model=IncidentResponse)
def create_incident(
    payload: IncidentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "analyst")),
):
    incident = Incident(**payload.model_dump())
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident


@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@router.put("/{incident_id}", response_model=IncidentResponse)
def update_incident(
    incident_id: int,
    payload: IncidentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "analyst")),
):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(incident, key, value)

    db.commit()
    db.refresh(incident)
    return incident


@router.delete("/{incident_id}")
def delete_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    db.delete(incident)
    db.commit()
    return {"status": "deleted"}


@router.get("/{incident_id}/comments", response_model=list[CommentResponse])
def get_comments(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Comment)
        .filter(Comment.incident_id == incident_id)
        .order_by(Comment.created_at.asc())
        .all()
    )


@router.post("/{incident_id}/comments", response_model=CommentResponse)
def add_comment(
    incident_id: int,
    payload: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "analyst")),
):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    comment = Comment(
        incident_id=incident_id,
        author=current_user.username,
        body=payload.body,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment
