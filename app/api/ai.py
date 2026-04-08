from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.ai import TriageRequest, TriageResponse
from app.services.ai_service import triage_alert

router = APIRouter(tags=["ai"])


@router.post("/triage", response_model=TriageResponse)
def triage(payload: TriageRequest, current_user: User = Depends(get_current_user)):
    return triage_alert(payload.text)
