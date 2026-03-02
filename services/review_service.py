from repositories.review_repository import ReviewRepository

class ReviewService:

    @staticmethod
    def add_review(user_id: str, book_id: str, text: str):
        return ReviewRepository.add_review(book_id, user_id, text)

    @staticmethod
    def list_reviews(book_id: str):
        return ReviewRepository.get_book_reviews(book_id)

    @staticmethod
    def delete_review(user, review_id: str):
        data = ReviewRepository.delete_review(review_id)
        if user["role"] != "admin" and data["user_id"] != user["sub"]:
            return {"error": "Not allowed"}
        return {"message": "Review deleted"}