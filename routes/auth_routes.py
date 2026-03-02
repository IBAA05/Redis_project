from fastapi import APIRouter
from models.user import User
from services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(user: User):
    return AuthService.register(user)


@router.post("/login")
def login(username: str, password: str):
    return AuthService.login(username, password)