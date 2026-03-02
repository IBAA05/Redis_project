from fastapi import HTTPException
from models.user import User
from repositories.user_repository import UserRepository
from core.security import hash_password, verify_password, create_access_token


class AuthService:

    @staticmethod
    def register(user: User):
        if UserRepository.find(user.username):
            raise HTTPException(status_code=400, detail="User already exists")

        user.password = hash_password(user.password)
        UserRepository.save(user)
        return {"message": "User registered successfully"}

    @staticmethod
    def login(username: str, password: str):
        user = UserRepository.find(username)
        if not user or not verify_password(password, user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token({
            "sub": username,
            "role": user["role"]
        })
        return {"access_token": token, "token_type": "bearer"}