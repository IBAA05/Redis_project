from fastapi import APIRouter
from services.reading_list_service import ReadingListService

router = APIRouter(prefix="/readinglists", tags=["Reading Lists"])

@router.post("/{user_id}/{list_name}")
def create_list(user_id: str, list_name: str):
    return ReadingListService.create_list(user_id, list_name)

@router.delete("/{user_id}/{list_name}")
def delete_list(user_id: str, list_name: str):
    return ReadingListService.delete_list(user_id, list_name)

@router.get("/{user_id}")
def get_user_lists(user_id: str):
    return ReadingListService.get_user_lists(user_id)

@router.post("/{user_id}/{list_name}/{book_id}")
def add_book(user_id: str, list_name: str, book_id: str):
    return ReadingListService.add_book(user_id, list_name, book_id)

@router.delete("/{user_id}/{list_name}/{book_id}")
def remove_book(user_id: str, list_name: str, book_id: str):
    return ReadingListService.remove_book(user_id, list_name, book_id)

@router.get("/{user_id}/{list_name}")
def get_books(user_id: str, list_name: str):
    return ReadingListService.get_books(user_id, list_name)