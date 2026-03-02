from pydantic import BaseModel
from typing import Literal

class ReadingStatus(BaseModel):
    book_id: str
    status: Literal["to_read", "reading", "finished"]