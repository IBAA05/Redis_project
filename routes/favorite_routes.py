from fastapi import APIRouter
from services.favorite_service import FavoriteService

router = APIRouter(prefix="/favorites", tags=["Favorites"])

@router.post("/{user_id}/{book_id}")
def add_favorite(user_id: str, book_id: str):
    return FavoriteService.add_favorite(user_id, book_id)

@router.delete("/{user_id}/{book_id}")
def remove_favorite(user_id: str, book_id: str):
    return FavoriteService.remove_favorite(user_id, book_id)

@router.get("/{user_id}")
def get_favorites(user_id: str):
    return FavoriteService.get_favorites(user_id)