from core.redis import redis_client
from datetime import datetime
import json

LOG_KEY = "audit_log"

class LogRepository:

    @staticmethod
    def add_log(action: str, description: str, book_id: str = None):
        entry = {
            "action": action,
            "description": description,
            "book_id": book_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        redis_client.lpush(LOG_KEY, json.dumps(entry))

    @staticmethod
    def get_recent(n: int):
        logs = redis_client.lrange(LOG_KEY, 0, n - 1)
        return [json.loads(log) for log in logs]

    @staticmethod
    def get_by_book(book_id: str):
        all_logs = redis_client.lrange(LOG_KEY, 0, -1)
        return [
            json.loads(log) for log in all_logs
            if json.loads(log).get("book_id") == book_id
        ]