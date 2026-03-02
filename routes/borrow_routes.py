from fastapi import APIRouter, Depends
from services.borrow_service import BorrowService
from models.borrow import Borrow
from core.dependencies import get_current_user, admin_only

router = APIRouter(prefix="/borrows", tags=["Borrow & Return"])


@router.post("/borrow")
def borrow_book(borrow: Borrow, user=Depends(get_current_user)):
    return BorrowService.borrow_book(user["sub"], borrow.book_id, borrow.due_date)


@router.post("/return/{book_id}")
def return_book(book_id: str, user=Depends(get_current_user)):
    return BorrowService.return_book(user["sub"], book_id)


@router.get("/me")
def my_borrows(user=Depends(get_current_user)):
    return BorrowService.get_my_borrows(user["sub"])


@router.get("/all", dependencies=[Depends(admin_only)])
def all_borrows():
    return BorrowService.get_all_borrows()