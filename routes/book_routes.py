from fastapi import APIRouter, HTTPException
from typing import Optional, List
from models.book import Book
from repositories.book_repository import BookRepository
from services.log_service import LogService

router = APIRouter()

@router.post("/books/", tags=["Management"])
def add_book(book: Book):
    existing = BookRepository.find_by_id(book.id)
    if existing:
        raise HTTPException(status_code=400, detail="Book ID already exists!")
    BookRepository.save(book)
    LogService.log("BOOK_ADDED", f"Book '{book.title}' was added", book.id)
    return {"message": "Book added successfully", "book": book}

@router.get("/books/search", tags=["Search & Filter"])
def search_by_title(title: str):
    all_books = BookRepository.get_all()
    results = [b for b in all_books if title.lower() in b["title"].lower()]
    if not results:
        raise HTTPException(status_code=404, detail="No books found with that title")
    return results

@router.put("/books/{book_id}", tags=["Management"])
def update_book(book_id: str, updated_data: Book):
    existing = BookRepository.find_by_id(book_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Book not found")
    BookRepository.update(book_id, updated_data)
    LogService.log("BOOK_UPDATED", f"Book '{book_id}' was updated", book_id)
    return {"message": "Book updated successfully"}

@router.delete("/books/{book_id}", tags=["Management"])
def delete_book(book_id: str):
    existing = BookRepository.find_by_id(book_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Book not found")
    BookRepository.delete(book_id)
    LogService.log("BOOK_DELETED", f"Book '{book_id}' was deleted", book_id)
    return {"message": "Book deleted successfully"}

@router.get("/books/", tags=["Listing"])
def list_all_books():
    return BookRepository.get_all()

@router.get("/books/filter", tags=["Search & Filter"])
def filter_books(author: Optional[str] = None, year: Optional[int] = None):
    books = BookRepository.get_all()
    if author:
        books = [b for b in books if author.lower() in b["author"].lower()]
    if year:
        books = [b for b in books if b["year"] == year]
    return books