from core.redis import redis_client
from uuid import uuid4
from datetime import date

class ReviewRepository:

    @staticmethod
    def add_review(book_id: str, user_id: str, text: str):
        review_id = str(uuid4())
        redis_client.hset(
            f"review:{review_id}",
            mapping={
                "review_id": review_id,
                "book_id": book_id,
                "user_id": user_id,
                "text": text,
                "date": str(date.today())
            }
        )
        redis_client.sadd(f"book:{book_id}:reviews", review_id)
        return review_id

    @staticmethod
    def get_book_reviews(book_id: str):
        ids = redis_client.smembers(f"book:{book_id}:reviews")
        return [redis_client.hgetall(f"review:{rid}") for rid in ids]

    @staticmethod
    def delete_review(review_id: str):
        data = redis_client.hgetall(f"review:{review_id}")
        redis_client.srem(f"book:{data['book_id']}:reviews", review_id)
        redis_client.delete(f"review:{review_id}")
        return data