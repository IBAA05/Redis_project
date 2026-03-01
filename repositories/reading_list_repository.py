from core.redis import redis_client

class ReadingListRepository:

    @staticmethod
    def create_list(user_id: str, list_name: str):
        redis_client.sadd(f"readinglists:{user_id}", list_name)

    @staticmethod
    def delete_list(user_id: str, list_name: str):
        redis_client.srem(f"readinglists:{user_id}", list_name)
        redis_client.delete(f"readinglist:{user_id}:{list_name}")

    @staticmethod
    def get_user_lists(user_id: str):
        return redis_client.smembers(f"readinglists:{user_id}")

    @staticmethod
    def list_exists(user_id: str, list_name: str) -> bool:
        return redis_client.sismember(f"readinglists:{user_id}", list_name)

    @staticmethod
    def add_book(user_id: str, list_name: str, book_id: str):
        redis_client.sadd(f"readinglist:{user_id}:{list_name}", book_id)

    @staticmethod
    def remove_book(user_id: str, list_name: str, book_id: str):
        redis_client.srem(f"readinglist:{user_id}:{list_name}", book_id)

    @staticmethod
    def get_books(user_id: str, list_name: str):
        return redis_client.smembers(f"readinglist:{user_id}:{list_name}")