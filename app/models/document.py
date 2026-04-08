from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.db.session import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    uploaded_by = Column(String(100), nullable=True)
    path = Column(String(500), nullable=True)
    document_type = Column(String(100), nullable=True, default="general")
    indexed = Column(String(10), nullable=False, default="false")
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
