from fastapi import APIRouter, Depends
from models.review import Review
from services.review_service import ReviewService
from core.dependencies import get_current_user

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/")
def add(review: Review, user=Depends(get_current_user)):
    return ReviewService.add_review(user["sub"], review.book_id, review.text)

@router.get("/{book_id}")
def list_reviews(book_id: str):
    return ReviewService.list_reviews(book_id)