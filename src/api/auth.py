from typing import Annotated
from fastapi import APIRouter, Form, Response

from src.api.dependencies import DBDep, UserIdDep
from src.services.auth import AuthService
from src.exceptions import (
    PasswordsNotMatchException,
    PasswordsNotMatchHttpException,
    UserAuthException,
    UserAuthHttpException,
    UserDuplicateException,
    UserDuplicateHttpException,
    UserNotFoundException,
    UserNotFoundHttpException,
)
from src.schemas.users import (
    UserLoginSchema,
    UserRequestAddSchema,
)
from src.config import settings


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def create_user(data: UserRequestAddSchema, db: DBDep):
    try:
        return await AuthService(db).create_user(data)
    except PasswordsNotMatchException:
        raise PasswordsNotMatchHttpException
    except UserDuplicateException:
        raise UserDuplicateHttpException


@router.post("/login")
async def authenticate_user(
    data: Annotated[UserLoginSchema, Form()], response: Response, db: DBDep
):
    try:
        access_token = await AuthService(db).authenticate_user(data)
        response.set_cookie(
            key="access_token",
            value=access_token,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            httponly=True,
        )
        return {"access_token": access_token}
    except UserAuthException:
        raise UserAuthHttpException


@router.post("/logout", summary="Logout User")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}


@router.get("/me", summary="Get Current User")
async def get_me(user_id: UserIdDep, db: DBDep):
    try:
        return await AuthService(db).me(user_id)
    except UserNotFoundException:
        raise UserNotFoundHttpException
