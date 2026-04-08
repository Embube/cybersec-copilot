from sqlalchemy.orm import Session

from app.db.session import Base, engine
from app.models.user import User
from app.core.security import get_password_hash


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

    # Seed default admin if absent
    from app.db.session import SessionLocal
    db: Session = SessionLocal()
    try:
        existing = db.query(User).filter(User.username == "admin").first()
        if not existing:
            admin = User(
                username="admin",
                email="admin@example.com",
                full_name="Default Admin",
                hashed_password=get_password_hash("Admin123!"),
                role="admin",
                is_active=True,
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()
