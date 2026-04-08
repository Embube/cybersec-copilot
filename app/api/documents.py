from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.document import Document
from app.models.user import User

router = APIRouter(tags=["documents"])


@router.get("/")
def list_documents(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Document).order_by(Document.uploaded_at.desc()).all()


@router.post("/seed")
def seed_documents(db: Session = Depends(get_db), current_user: User = Depends(require_roles("admin", "analyst"))):
    docs = [
        Document(filename="password_policy.pdf", uploaded_by=current_user.username, document_type="policy", indexed="false"),
        Document(filename="phishing_playbook.pdf", uploaded_by=current_user.username, document_type="playbook", indexed="false"),
    ]
    for doc in docs:
        db.add(doc)
    db.commit()
    return {"status": "seeded", "count": len(docs)}
