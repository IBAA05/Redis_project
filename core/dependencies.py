from fastapi import Depends, HTTPException, Header
from jose import JWTError
from core.security import decode_token


def get_current_user(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
        payload = decode_token(token)
        return payload
    except (JWTError, IndexError):
        raise HTTPException(status_code=401, detail="Invalid or missing token")


def admin_only(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
