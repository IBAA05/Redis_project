from repositories.rating_repository import RatingRepository

class RatingService:

    @staticmethod
    def rate_book(user_id: str, book_id: str, score: int):
        if not RatingRepository.add_rating(book_id, user_id, score):
            return {"error": "You already rated this book"}
        return {"message": "Rating submitted"}

    @staticmethod
    def get_rating(book_id: str):
        return RatingRepository.get_stats(book_id)