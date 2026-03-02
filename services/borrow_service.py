from repositories.borrow_repository import BorrowRepository
from repositories.book_repository import BookRepository
from datetime import date
from services.log_service import LogService
from models.book import Book


class BorrowService:

    @staticmethod
    def borrow_book(user_id: str, book_id: str, due_date: date):
        book = BookRepository.find_by_id(book_id)
        if not book:
            return {"error": "Book not found"}

        if BorrowRepository.find_borrow(book_id):
            return {"error": "Book already borrowed"}

        if book["stock"] <= 0:
            return {"error": "Book out of stock"}

        # Update stock
        book["stock"] -= 1
        BookRepository.update(book_id, Book(**book))

        BorrowRepository.borrow(user_id, book_id, due_date)
        LogService.log("BOOK_BORROWED", f"{user_id} borrowed {book['title']}", book_id)

        return {"message": "Book borrowed successfully"}

    @staticmethod
    def return_book(user_id: str, book_id: str):
        borrow = BorrowRepository.find_borrow(book_id)
        if not borrow:
            return {"error": "Book not borrowed"}

        if borrow["user_id"] != user_id:
            return {"error": "You cannot return a book you did not borrow"}

        book = BookRepository.find_by_id(book_id)
        book["stock"] += 1
        BookRepository.update(book_id, Book(**book))

        BorrowRepository.return_book(user_id, book_id)
        LogService.log("BOOK_RETURNED", f"{user_id} returned {book['title']}", book_id)

        return {"message": "Book returned successfully"}

    @staticmethod
    def get_all_borrows():  # ADMIN
        return BorrowRepository.get_all_borrows()

    @staticmethod
    def get_my_borrows(user_id: str):  # USER
        return BorrowRepository.get_user_borrows(user_id)