from core.redis import redis_client
from datetime import date

BORROW_KEY = "borrows"


class BorrowRepository:

    @staticmethod
    def borrow(user_id: str, book_id: str, due_date: date):
        redis_client.hset(
            f"borrow:{book_id}",
            mapping={
                "user_id": user_id,
                "book_id": book_id,
                "borrow_date": str(date.today()),
                "due_date": str(due_date),
            }
        )

        # Global index (admin)
        redis_client.sadd(BORROW_KEY, book_id)

        # User index (per-user)
        redis_client.sadd(f"user:{user_id}:borrows", book_id)

    @staticmethod
    def return_book(user_id: str, book_id: str):
        redis_client.delete(f"borrow:{book_id}")
        redis_client.srem(BORROW_KEY, book_id)
        redis_client.srem(f"user:{user_id}:borrows", book_id)

    @staticmethod
    def find_borrow(book_id: str):
        data = redis_client.hgetall(f"borrow:{book_id}")
        return data if data else None

    @staticmethod
    def get_all_borrows():
        book_ids = redis_client.smembers(BORROW_KEY)
        return [redis_client.hgetall(f"borrow:{bid}") for bid in book_ids]

    @staticmethod
    def get_user_borrows(user_id: str):
        book_ids = redis_client.smembers(f"user:{user_id}:borrows")
        return [redis_client.hgetall(f"borrow:{bid}") for bid in book_ids]