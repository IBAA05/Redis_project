import json
from typing import List
from fastapi import HTTPException
from models.book import Book
from repositories.book_repository import BookRepository


class BookService:

    @staticmethod
    def add_book(book: Book):
        if BookRepository.find_by_id(book.id):
            raise HTTPException(status_code=400, detail="Book already exists")
        BookRepository.save(book)
        return book

    @staticmethod
    def list_books() -> List[dict]:
        return [json.loads(b) for b in BookRepository.get_all()]

    @staticmethod
    def update_book(book_id: str, book: Book):
        if not BookRepository.find_by_id(book_id):
            raise HTTPException(status_code=404, detail="Book not found")
        BookRepository.update(book_id, book)

    @staticmethod
    def delete_book(book_id: str):
        if not BookRepository.find_by_id(book_id):
            raise HTTPException(status_code=404, detail="Book not found")
        BookRepository.delete(book_id)

    @staticmethod
    def search(title: str):
        books = BookService.list_books()
        return [b for b in books if title.lower() in b["title"].lower()]

    @staticmethod
    def filter(author: str = None, year: int = None):
        books = BookService.list_books()
        if author:
            books = [b for b in books if author.lower() in b["author"].lower()]
        if year:
            books = [b for b in books if b["year"] == year]
        return books