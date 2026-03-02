from fastapi import APIRouter
from services.log_service import LogService

router = APIRouter(prefix="/logs", tags=["Audit Log"])

@router.get("/recent")
def get_recent_logs(n: int = 10):
    return LogService.get_recent(n)

@router.get("/book/{book_id}")
def get_logs_by_book(book_id: str):
    return LogService.get_by_book(book_id)