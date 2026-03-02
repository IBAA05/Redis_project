from core.redis import redis_client

class RatingRepository:

    @staticmethod
    def add_rating(book_id: str, user_id: str, score: int):
        key = f"rating:{book_id}"

        if redis_client.hexists(key, user_id):
            return False

        redis_client.hset(key, user_id, score)
        redis_client.incr(f"{key}:count")
        redis_client.incrby(f"{key}:sum", score)
        return True

    @staticmethod
    def get_stats(book_id: str):
        count = int(redis_client.get(f"rating:{book_id}:count") or 0)
        total = int(redis_client.get(f"rating:{book_id}:sum") or 0)
        avg = round(total / count, 2) if count > 0 else 0
        return {"average": avg, "count": count}