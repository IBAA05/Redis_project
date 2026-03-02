from fastapi import APIRouter, Depends
from models.book import Book
from services.book_service import BookService
from core.dependencies import admin_only

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", dependencies=[Depends(admin_only)])
def add_book(book: Book):
    return BookService.add_book(book)


@router.put("/{book_id}", dependencies=[Depends(admin_only)])
def update_book(book_id: str, book: Book):
    BookService.update_book(book_id, book)
    return {"message": "Book updated"}


@router.delete("/{book_id}", dependencies=[Depends(admin_only)])
def delete_book(book_id: str):
    BookService.delete_book(book_id)
    return {"message": "Book deleted"}


@router.get("/")
def list_books():
    return BookService.list_books()


@router.get("/search")
def search_books(title: str):
    return BookService.search(title)


@router.get("/filter")
def filter_books(author: str = None, year: int = None):
    return BookService.filter(author, year)