from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: str
    username: str
    password: str
    role: str = "user"  # user | admin