from pydantic import BaseModel

class Favorite(BaseModel):
    user_id: str
    book_id: str