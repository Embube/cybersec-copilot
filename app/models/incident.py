from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.db.session import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    source = Column(String(255), nullable=False, default="Manual")
    severity = Column(String(50), nullable=False, default="Medium")
    threat_type = Column(String(100), nullable=False, default="Unknown")
    summary = Column(Text, nullable=False)
    analyst_notes = Column(Text, nullable=True)
    raw_event = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="Open")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
