from core.redis import redis_client

AUDIT_STREAM = "audit_stream"
OVERDUE_STREAM = "overdue_stream"


class StreamRepository:

    # ─── General publish ───────────────────────────────────────────────────────

    @staticmethod
    def publish(stream: str, fields: dict) -> str:
        """XADD stream * field value … — returns the generated message ID."""
        return redis_client.xadd(stream, fields)

    # ─── Read helpers ──────────────────────────────────────────────────────────

    @staticmethod
    def read_range(stream: str, start: str = "-", end: str = "+", count: int = 100) -> list:
        """XRANGE — oldest to newest."""
        return redis_client.xrange(stream, min=start, max=end, count=count)

    @staticmethod
    def read_latest(stream: str, count: int = 50) -> list:
        """XREVRANGE — newest first."""
        return redis_client.xrevrange(stream, max="+", min="-", count=count)

    @staticmethod
    def stream_length(stream: str) -> int:
        """XLEN — total number of messages in the stream."""
        return redis_client.xlen(stream)

    # ─── Consumer Group helpers ────────────────────────────────────────────────

    @staticmethod
    def create_consumer_group(stream: str, group: str, start_id: str = "0") -> bool:
        """
        XGROUP CREATE — idempotent: returns False if the group already exists.
        Uses MKSTREAM so the stream is created automatically if absent.
        """
        try:
            redis_client.xgroup_create(stream, group, id=start_id, mkstream=True)
            return True
        except Exception:
            # BUSYGROUP — group already exists, which is fine
            return False

    @staticmethod
    def read_group(stream: str, group: str, consumer: str, count: int = 10) -> list:
        """XREADGROUP — reads unacknowledged messages for this consumer."""
        result = redis_client.xreadgroup(
            groupname=group,
            consumername=consumer,
            streams={stream: ">"},
            count=count,
            block=0,        # non-blocking
        )
        if result:
            # result format: [(stream_name, [(id, fields), ...])]
            return result[0][1]
        return []

    @staticmethod
    def ack(stream: str, group: str, *message_ids) -> int:
        """XACK — acknowledge processed messages."""
        return redis_client.xack(stream, group, *message_ids)
