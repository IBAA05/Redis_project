from fastapi import APIRouter, Depends
from services.favorite_service import FavoriteService
from core.dependencies import get_current_user

router = APIRouter(prefix="/favorites", tags=["Favorites"])

@router.post("/{book_id}")
def add_favorite(
    book_id: str,
    user: dict = Depends(get_current_user)
):
    user_id = user["sub"]
    return FavoriteService.add_favorite(user_id, book_id)


@router.delete("/{book_id}")
def remove_favorite(
    book_id: str,
    user: dict = Depends(get_current_user)
):
    user_id = user["sub"]
    return FavoriteService.remove_favorite(user_id, book_id)


@router.get("/")
def get_favorites(
    user: dict = Depends(get_current_user)
):
    user_id = user["sub"]
    return FavoriteService.get_favorites(user_id)