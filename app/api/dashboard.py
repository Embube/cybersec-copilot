from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.dashboard import DashboardMetricsResponse
from app.services.dashboard_service import build_dashboard_metrics

router = APIRouter(tags=["dashboard"])


@router.get("/metrics", response_model=DashboardMetricsResponse)
def metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return build_dashboard_metrics(db)
