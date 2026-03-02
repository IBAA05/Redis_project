from pydantic import BaseModel
from datetime import date

class Review(BaseModel):
    book_id: str
    text: str