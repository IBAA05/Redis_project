from core.redis import redis_client
from repositories.stream_repository import StreamRepository, OVERDUE_STREAM

OVERDUE_GROUP = "overdue_processors"
OVERDUE_CONSUMER = "worker-1"


class OverdueConsumer:

    @staticmethod
    def process_overdue_events() -> dict:
        """
        Reads unacknowledged events from `overdue_stream` using a consumer group,
        marks each borrow hash with  status = overdue  in Redis,
        then ACKs the message so it is not reprocessed.

        Returns { "processed": int, "details": list }
        """
        # Ensure the consumer group exists (idempotent)
        StreamRepository.create_consumer_group(OVERDUE_STREAM, OVERDUE_GROUP, start_id="0")

        messages = StreamRepository.read_group(
            OVERDUE_STREAM, OVERDUE_GROUP, OVERDUE_CONSUMER, count=100
        )

        processed = []

        for msg_id, fields in messages:
            book_id = fields.get("book_id", "")
            days_overdue = fields.get("days_overdue", "0")

            if book_id:
                # Mark the borrow hash with overdue status
                redis_client.hset(f"borrow:{book_id}", "status", "overdue")

            StreamRepository.ack(OVERDUE_STREAM, OVERDUE_GROUP, msg_id)

            processed.append({
                "msg_id": msg_id,
                "book_id": book_id,
                "user_id": fields.get("user_id", ""),
                "due_date": fields.get("due_date", ""),
                "days_overdue": int(days_overdue),
            })

        return {"processed": len(processed), "details": processed}

    @staticmethod
    def list_overdue_borrows() -> list:
        """
        Scans all borrow hashes and returns those with status = overdue.
        """
        # Collect every known borrow key from the global borrow set
        book_ids = redis_client.smembers("borrows")
        overdue = []
        for book_id in book_ids:
            data = redis_client.hgetall(f"borrow:{book_id}")
            if data.get("status") == "overdue":
                overdue.append(data)
        return overdue
