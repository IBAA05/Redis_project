from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LogEntry(BaseModel):
    action: str
    description: str
    book_id: Optional[str] = None
    timestamp: str = ""