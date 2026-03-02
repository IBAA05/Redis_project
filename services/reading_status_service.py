from repositories.reading_status_repository import ReadingStatusRepository

class ReadingStatusService:

    @staticmethod
    def update(user_id: str, book_id: str, status: str):
        ReadingStatusRepository.update_status(user_id, book_id, status)
        return {"message": "Status updated"}

    @staticmethod
    def list(user_id: str, status: str):
        return ReadingStatusRepository.get_by_status(user_id, status)