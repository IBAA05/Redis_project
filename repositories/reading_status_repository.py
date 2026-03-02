from core.redis import redis_client

class ReadingStatusRepository:

    @staticmethod
    def update_status(user_id: str, book_id: str, status: str):
        old = redis_client.hget(f"user:{user_id}:book_status", book_id)
        if old:
            redis_client.srem(f"user:{user_id}:status:{old}", book_id)

        redis_client.hset(f"user:{user_id}:book_status", book_id, status)
        redis_client.sadd(f"user:{user_id}:status:{status}", book_id)

    @staticmethod
    def get_by_status(user_id: str, status: str):
        return list(redis_client.smembers(f"user:{user_id}:status:{status}"))