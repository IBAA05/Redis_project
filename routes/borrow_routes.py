from fastapi import APIRouter
from services.borrow_service import BorrowService
from models.borrow import Borrow

router = APIRouter(prefix="/borrows", tags=["Borrow & Return"])

@router.post("/borrow")
def borrow_book(borrow: Borrow):
    return BorrowService.borrow_book(borrow.user_id, borrow.book_id, borrow.due_date)

@router.post("/return/{book_id}")
def return_book(book_id: str):
    return BorrowService.return_book(book_id)

@router.get("/all")
def get_all_borrows():
    return BorrowService.get_all_borrows()

@router.get("/overdue")
def get_overdue_books():
    return BorrowService.get_overdue_books()