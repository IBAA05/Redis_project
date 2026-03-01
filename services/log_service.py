from repositories.log_repository import LogRepository

class LogService:

    @staticmethod
    def log(action: str, description: str, book_id: str = None):
        LogRepository.add_log(action, description, book_id)

    @staticmethod
    def get_recent(n: int = 10):
        return LogRepository.get_recent(n)

    @staticmethod
    def get_by_book(book_id: str):
        return LogRepository.get_by_book(book_id)