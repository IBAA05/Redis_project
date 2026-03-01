from repositories.reading_list_repository import ReadingListRepository
from repositories.book_repository import BookRepository

class ReadingListService:

    @staticmethod
    def create_list(user_id: str, list_name: str):
        if ReadingListRepository.list_exists(user_id, list_name):
            return {"error": f"List '{list_name}' already exists"}
        ReadingListRepository.create_list(user_id, list_name)
        return {"message": f"List '{list_name}' created successfully"}

    @staticmethod
    def delete_list(user_id: str, list_name: str):
        if not ReadingListRepository.list_exists(user_id, list_name):
            return {"error": f"List '{list_name}' not found"}
        ReadingListRepository.delete_list(user_id, list_name)
        return {"message": f"List '{list_name}' deleted successfully"}

    @staticmethod
    def get_user_lists(user_id: str):
        return list(ReadingListRepository.get_user_lists(user_id))

    @staticmethod
    def add_book(user_id: str, list_name: str, book_id: str):
        if not ReadingListRepository.list_exists(user_id, list_name):
            return {"error": f"List '{list_name}' not found"}
        book = BookRepository.find_by_id(book_id)
        if not book:
            return {"error": "Book not found"}
        ReadingListRepository.add_book(user_id, list_name, book_id)
        return {"message": f"Book '{book['title']}' added to list '{list_name}'"}

    @staticmethod
    def remove_book(user_id: str, list_name: str, book_id: str):
        if not ReadingListRepository.list_exists(user_id, list_name):
            return {"error": f"List '{list_name}' not found"}
        books = ReadingListRepository.get_books(user_id, list_name)
        if book_id not in books:
            return {"error": "Book is not in this list"}
        ReadingListRepository.remove_book(user_id, list_name, book_id)
        return {"message": "Book removed from list"}

    @staticmethod
    def get_books(user_id: str, list_name: str):
        if not ReadingListRepository.list_exists(user_id, list_name):
            return {"error": f"List '{list_name}' not found"}
        book_ids = ReadingListRepository.get_books(user_id, list_name)
        books = []
        for book_id in book_ids:
            book = BookRepository.find_by_id(book_id)
            if book:
                books.append(book)
        return books