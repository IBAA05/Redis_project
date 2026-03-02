from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class Borrow(BaseModel):
    book_id: str
    due_date: date
    # These are filled internally (not from request body)
    user_id: Optional[str] = Field(default=None)
    borrow_date: Optional[date] = Field(default=None)