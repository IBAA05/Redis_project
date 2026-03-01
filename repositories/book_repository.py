import json
from typing import List, Optional
from core.redis import redis_client
from models.book import Book

BOOK_KEY = "books"


class BookRepository:

    @staticmethod
    def get_all() -> List[dict]:
        return redis_client.lrange(BOOK_KEY, 0, -1)

    @staticmethod
    def save(book: Book):
        redis_client.rpush(BOOK_KEY, book.model_dump_json())

    @staticmethod
    def find_by_id(book_id: str) -> Optional[dict]:
        books = redis_client.lrange(BOOK_KEY, 0, -1)
        for b in books:
            book = json.loads(b)
            if book["id"] == book_id:
                return book
        return None

    @staticmethod
    def update(book_id: str, updated_book: Book):
        books = redis_client.lrange(BOOK_KEY, 0, -1)
        redis_client.delete(BOOK_KEY)

        for b in books:
            book = json.loads(b)
            if book["id"] == book_id:
                redis_client.rpush(BOOK_KEY, updated_book.model_dump_json())
            else:
                redis_client.rpush(BOOK_KEY, json.dumps(book))

    @staticmethod
    def delete(book_id: str):
        books = redis_client.lrange(BOOK_KEY, 0, -1)
        redis_client.delete(BOOK_KEY)

        for b in books:
            book = json.loads(b)
            if book["id"] != book_id:
                redis_client.rpush(BOOK_KEY, json.dumps(book))