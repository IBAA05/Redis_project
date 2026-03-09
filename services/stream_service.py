from datetime import datetime
from repositories.stream_repository import StreamRepository, AUDIT_STREAM


class StreamService:

    # ─── Publish ───────────────────────────────────────────────────────────────

    @staticmethod
    def publish_event(
        action: str,
        description: str,
        book_id: str = "",
        user_id: str = "",
    ) -> str:
        """
        Publish a structured event to the audit_stream.
        Returns the Redis message ID (e.g. "1709999999999-0").
        """
        fields = {
            "action": action,
            "description": description,
            "book_id": book_id or "",
            "user_id": user_id or "",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        return StreamRepository.publish(AUDIT_STREAM, fields)

    # ─── Query ─────────────────────────────────────────────────────────────────

    @staticmethod
    def get_all_events(count: int = 50) -> list:
        """Return the most recent `count` events (newest first)."""
        raw = StreamRepository.read_latest(AUDIT_STREAM, count=count)
        return [{"id": msg_id, **fields} for msg_id, fields in raw]

    @staticmethod
    def get_events_by_book(book_id: str, count: int = 50) -> list:
        """Return events filtered to a specific book_id (newest first)."""
        raw = StreamRepository.read_latest(AUDIT_STREAM, count=count)
        return [
            {"id": msg_id, **fields}
            for msg_id, fields in raw
            if fields.get("book_id") == book_id
        ]

    @staticmethod
    def get_stream_info() -> dict:
        """Return basic metadata about the audit stream."""
        length = StreamRepository.stream_length(AUDIT_STREAM)
        return {
            "stream": AUDIT_STREAM,
            "total_events": length,
        }
