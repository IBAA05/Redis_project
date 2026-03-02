from pydantic import BaseModel, Field

class Rating(BaseModel):
    book_id: str
    score: int = Field(..., ge=1, le=5)
