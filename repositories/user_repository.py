import json
from core.redis import redis_client
from models.user import User

USER_KEY = "users"


class UserRepository:

    @staticmethod
    def save(user: User):
        redis_client.hset(USER_KEY, user.username, user.model_dump_json())

    @staticmethod
    def find(username: str):
        user = redis_client.hget(USER_KEY, username)
        return json.loads(user) if user else None