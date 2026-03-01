from pydantic import BaseModel, Field
from typing import Optional

class Book(BaseModel):
    id: str
    title: str
    author: str
    year: int

    rating: Optional[float] = Field(None, ge=0, le=5)
    comment: Optional[str] = None
    status: str = Field(default="available")  # available | borrowed
    stock: int = Field(default=1, ge=0)