from pydantic import BaseModel
from typing import List, Optional

class ReadingList(BaseModel):
    user_id: str
    list_name: str

class ReadingListItem(BaseModel):
    user_id: str
    list_name: str
    book_id: str