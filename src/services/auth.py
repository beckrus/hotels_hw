from typing import Annotated
from fastapi import Depends
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError

from src.services.exceptions import InvalidTokenDataError
from src.config import settings


class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password:str, hashed_password:str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)


    def hash_password(self, password:str) -> str:
        return self.pwd_context.hash(password)


    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt
    
    def get_current_user(self, token: str):
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            user_id = payload.get("user_id")
            if user_id is None:
                raise InvalidTokenDataError
            return user_id
        except InvalidTokenError:
            raise InvalidTokenDataError
        