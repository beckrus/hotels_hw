from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt

from src.exceptions import (
    DuplicateItemException,
    ItemNotFoundException,
    PasswordsNotMatchException,
    UserAuthException,
    UserDuplicateException,
    UserNotFoundException,
)
from src.schemas.users import (
    UserHashedPwdAddSchema,
    UserLoginSchema,
    UserRequestAddSchema,
)
from src.config import settings
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    def create_access_token(cls, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    @classmethod
    def decode_token(cls, token: str) -> dict[str, str | int]:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload

    async def create_user(self, data: UserRequestAddSchema):
        data.is_superuser = False
        data.is_varified = False
        if data.password != data.password_confirm:
            raise PasswordsNotMatchException
        hashed_password = self.hash_password(data.password.get_secret_value())
        user_data = UserHashedPwdAddSchema(
            **data.model_dump(), password_hash=hashed_password
        )

        try:
            user = await self.db.users.add(user_data)
            await self.db.commit()
            return user
        except DuplicateItemException as e:
            raise UserDuplicateException from e

    async def authenticate_user(self, data: UserLoginSchema) -> str:
        user = await self.db.users.get_one_with_hashed_password(username=data.username)
        if user and self.verify_password(data.password, user.password_hash):
            return AuthService.create_access_token({"user_id": user.id})
        raise UserAuthException

    async def me(self, user_id: int):
        try:
            user = await self.db.users.get_one_by_id(id=user_id)
            return user
        except ItemNotFoundException:
            UserNotFoundException
