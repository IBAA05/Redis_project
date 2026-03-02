from fastapi import APIRouter, Depends
from models.reading_status import ReadingStatus
from services.reading_status_service import ReadingStatusService
from core.dependencies import get_current_user

router = APIRouter(prefix="/reading-status", tags=["Reading Status"])

@router.post("/")
def update(status: ReadingStatus, user=Depends(get_current_user)):
    return ReadingStatusService.update(user["sub"], status.book_id, status.status)

@router.get("/{status}")
def list(status: str, user=Depends(get_current_user)):
    return ReadingStatusService.list(user["sub"], status)