from repositories.borrow_repository import BorrowRepository
from repositories.book_repository import BookRepository
from datetime import date
import json
from services.log_service import LogService
class BorrowService:

    @staticmethod
    def borrow_book(user_id: str, book_id: str, due_date: date):
        # Check book exists
        book = BookRepository.find_by_id(book_id)
        if not book:
            return {"error": "Book not found"}

        # Check if already borrowed
        existing = BorrowRepository.find_borrow(book_id)
        if existing:
            return {"error": f"Book is already borrowed by user '{existing['user_id']}'"}

        # Check stock availability
        if book["stock"] <= 0:
            return {"error": "Book is out of stock"}

        # Reduce stock by 1
        book["stock"] -= 1
        from models.book import Book
        BookRepository.update(book_id, Book(**book))
         
        # Save borrow record
        BorrowRepository.borrow(user_id, book_id, due_date)
        LogService.log("BOOK_BORROWED", f"Book '{book['title']}' borrowed by '{user_id}' until {due_date}", book_id)
        return {"message": f"Book '{book['title']}' borrowed successfully until {due_date}"}

    @staticmethod
    def return_book(book_id: str):
        # Check if actually borrowed
        existing = BorrowRepository.find_borrow(book_id)
        if not existing:
            return {"error": "Book is not currently borrowed"}

        # Restore stock by 1
        book = BookRepository.find_by_id(book_id)
        if book:
            book["stock"] += 1
            from models.book import Book
            BookRepository.update(book_id, Book(**book))

        BorrowRepository.return_book(book_id)
        LogService.log("BOOK_RETURNED", f"Book '{book['title']}' returned by user", book_id)
        return {"message": f"Book '{book['title']}' returned successfully"}

    @staticmethod
    def get_all_borrows():
        borrows = BorrowRepository.get_all_borrows()
        result = []
        for borrow in borrows:
            book = BookRepository.find_by_id(borrow["book_id"])
            if book:
                borrow["book_title"] = book["title"]
            result.append(borrow)
        return result

    @staticmethod
    def get_overdue_books():
        borrows = BorrowRepository.get_all_borrows()
        overdue = []
        today = date.today()
        for borrow in borrows:
            due = date.fromisoformat(borrow["due_date"])
            if due < today:
                book = BookRepository.find_by_id(borrow["book_id"])
                if book:
                    borrow["book_title"] = book["title"]
                overdue.append(borrow)
        return overdue