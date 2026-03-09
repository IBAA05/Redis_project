from datetime import date
from repositories.borrow_repository import BorrowRepository
from repositories.stream_repository import StreamRepository, OVERDUE_STREAM


class OverdueProducer:

    @staticmethod
    def scan_and_publish() -> dict:
        """
        Scans every active borrow and publishes an event to `overdue_stream`
        for each one whose due_date is strictly in the past.

        Returns a summary: { "scanned": int, "published": int, "overdue_book_ids": list }
        """
        all_borrows = BorrowRepository.get_all_borrows()
        today = date.today()
        published = []

        for borrow in all_borrows:
            if not borrow:
                continue

            due_date_str = borrow.get("due_date", "")
            try:
                due_date = date.fromisoformat(due_date_str)
            except ValueError:
                continue

            if due_date < today:
                days_overdue = (today - due_date).days
                book_id = borrow.get("book_id", "")
                user_id = borrow.get("user_id", "")

                StreamRepository.publish(OVERDUE_STREAM, {
                    "book_id": book_id,
                    "user_id": user_id,
                    "due_date": due_date_str,
                    "days_overdue": str(days_overdue),
                })
                published.append(book_id)

        return {
            "scanned": len(all_borrows),
            "published": len(published),
            "overdue_book_ids": published,
        }
