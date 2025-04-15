from typing import Annotated
from fastapi import APIRouter, Depends, Form, Response, Request

from src.api.dependencies import DBDep, UserIdDep, get_current_user, oauth2_scheme
from src.services.auth import AuthService
from src.exceptions import (
    PasswordsNotMatchException,
    PasswordsNotMatchHttpException,
    UserAlreadyAuthanticatedHttpException,
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
    # if not admin set is_superuser to False and is_verified to False
    try:
        return await AuthService(db).create_user(data)
    except PasswordsNotMatchException:
        raise PasswordsNotMatchHttpException
    except UserDuplicateException:
        raise UserDuplicateHttpException


@router.post("/login")
async def authenticate_user(
    data: Annotated[UserLoginSchema, Form()], request:Request,response: Response, db: DBDep
):
    token = request.cookies.get("access_token")
    print(token)
    if token:
        if get_current_user(request, token):
            raise UserAlreadyAuthanticatedHttpException
    try:
        access_token = await AuthService(db).authenticate_user(data)
        response.set_cookie(key="access_token", value=access_token, max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return {"access_token": access_token}
    except UserAuthException:
        raise UserAuthHttpException


@router.post("/logout", summary="Logout User")
async def logout_user(request: Request, response: Response, user_id: UserIdDep):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}


@router.get("/me", summary="Get Current User")
async def get_me(user_id: UserIdDep, db: DBDep):
    try:
        return await AuthService(db).me(user_id)
    except UserNotFoundException:
        raise UserNotFoundHttpException
