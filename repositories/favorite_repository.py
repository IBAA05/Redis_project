from core.redis import redis_client

class FavoriteRepository:

    @staticmethod
    def add(user_id: str, book_id: str):
        redis_client.sadd(f"favorites:{user_id}", book_id)

    @staticmethod
    def remove(user_id: str, book_id: str):
        redis_client.srem(f"favorites:{user_id}", book_id)

    @staticmethod
    def get_all(user_id: str):
        return redis_client.smembers(f"favorites:{user_id}")