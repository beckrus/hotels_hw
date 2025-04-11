from typing import Annotated, Any, AsyncGenerator
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import BaseModel
from fastapi import HTTPException, Query, Depends, Request

from src.exceptions import AccessForbiddenHttpException, TokenErrorHttpException
from src.repositories.users import UsersRepository
from src.services.auth import AuthService
from src.database import async_session_maker, async_session_maker_null_pool
from src.utils.db_manager import DBManager


class PaginationParamsSchema(BaseModel):
    page: Annotated[int, Query(description="Page", default=1, ge=1)]
    per_page: Annotated[int, Query(description="Limit", default=10, ge=1, lt=101)]


PaginationDep = Annotated[PaginationParamsSchema, Depends()]


class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    def __init__(self, tokenUrl: str, auto_error: bool = True):
        super().__init__(tokenUrl=tokenUrl, auto_error=auto_error)

    async def __call__(self, request: Request):
        token = request.cookies.get("access_token")
        if not token:
            if self.auto_error:
                raise HTTPException(
                    status_code=401, detail="Not authenticated, missing token"
                )
            else:
                return None
        return token


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="auth/login")


def get_current_user(request: Request, token: str = Depends(oauth2_scheme)) -> int:
    try:
        token_data = AuthService().decode_token(token)
        return token_data["user_id"]
    except InvalidTokenError:
        raise TokenErrorHttpException


async def get_admin_user(
    request: Request, user_id: str = Depends(get_current_user)
) -> int:
    async with async_session_maker() as session:
        users_repo = UsersRepository(session)
        user = await users_repo.get_one_by_id(user_id)
        if not user.is_superuser:
            raise AccessForbiddenHttpException
        return user_id


UserIdDep = Annotated[int, Depends(get_current_user)]

UserIdAdminDep = Annotated[int, Depends(get_admin_user)]


def get_db_manager() -> DBManager:
    return DBManager(session_factory=async_session_maker)


def get_db_manager_null_pull() -> DBManager:
    return DBManager(session_factory=async_session_maker_null_pool)


async def get_db() -> AsyncGenerator[DBManager, Any]:
    async with get_db_manager() as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
