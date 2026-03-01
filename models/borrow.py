from pydantic import BaseModel
from datetime import date

class Borrow(BaseModel):
    user_id: str
    book_id: str
    due_date: date