from fastapi import APIRouter, Depends
from models.rating import Rating
from services.rating_service import RatingService
from core.dependencies import get_current_user

router = APIRouter(prefix="/ratings", tags=["Ratings"])

@router.post("/")
def rate(rating: Rating, user=Depends(get_current_user)):
    return RatingService.rate_book(user["sub"], rating.book_id, rating.score)

@router.get("/{book_id}")
def stats(book_id: str):
    return RatingService.get_rating(book_id)