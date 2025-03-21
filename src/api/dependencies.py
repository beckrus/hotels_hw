from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import BaseModel
from fastapi import HTTPException, Query, Depends, Request

from src.services.auth import AuthService


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
                    status_code=401,
                    detail="Not authenticated, missing token"
                )
            else:
                return None
        return token
    
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="auth/login")


# def get_token(request: Request) -> str:
#     token = request.cookies.get('access_token')
#     if not token:
#         raise HTTPException(
#             status_code=401,
#             detail='Missing token'
#         )
#     return token


def get_current_user(request: Request, token: str = Depends(oauth2_scheme)) -> int:
    try:
        token_data = AuthService().decode_token(token)
        return token_data['user_id']
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail='Could not validate credentials'
        )
    
UserIdDep = Annotated[int, Depends(get_current_user)]

