from repositories.favorite_repository import FavoriteRepository
from repositories.book_repository import BookRepository
from services.log_service import LogService

class FavoriteService:

    @staticmethod
    def add_favorite(user_id: str, book_id: str):
        book = BookRepository.find_by_id(book_id)
        print(f"Looking for book_id: '{book_id}', found: {book}")
        if not book:
         return {"error": "Book not found"}
        FavoriteRepository.add(user_id, book_id)
        LogService.log("FAVORITE_ADDED", f"Book '{book['title']}' added to favorites by '{user_id}'", book_id)
        return {"message": f"Book '{book['title']}' added to favorites"}

    @staticmethod
    def remove_favorite(user_id: str, book_id: str):
        favorites = FavoriteRepository.get_all(user_id)
        if book_id not in favorites:
            return {"error": "Book is not in favorites"}
        FavoriteRepository.remove(user_id, book_id)
        LogService.log("FAVORITE_REMOVED", f"Book removed from favorites by '{user_id}'", book_id)
        return {"message": "Book removed from favorites"}

    @staticmethod
    def get_favorites(user_id: str):
        book_ids = FavoriteRepository.get_all(user_id)
        books = []
        for book_id in book_ids:
            book = BookRepository.find_by_id(book_id)
            if book:
                books.append(book)
        return books
