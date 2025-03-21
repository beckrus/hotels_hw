
from fastapi import APIRouter, HTTPException, Response, Request
from jwt import InvalidTokenError

from api.dependencies import UserIdDep
from src.services.auth import AuthService
from src.repositories.exceptions import DuplicateItemException, ItemNotFoundException
from src.repositories.users import UsersRepository
from src.schemas.users import UserHashedPwdAddSchema, UserLoginSchema, UserRequestAddSchema
from src.database import async_session_maker

router = APIRouter(prefix="/auth", tags=["Auth"])



@router.post("/register")
async def create_user(data: UserRequestAddSchema):
    # if not admin set is_superuser to False and is_verified to False
    data.is_superuser = False
    data.is_varified = False
    if data.password != data.password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    hashed_password = AuthService().hash_password(data.password.get_secret_value())
    user_data = UserHashedPwdAddSchema(**data.model_dump(), password_hash=hashed_password)

    try:
        async with async_session_maker() as session:
            users_repo = UsersRepository(session)
            user = await users_repo.add(user_data)
            await users_repo.commit()
            return user
    except DuplicateItemException:
        raise HTTPException(
            status_code=400,
            detail="User with these username, email or phone already exists",
        )

@router.post("/login")
async def authenticate_user(data: UserLoginSchema, response: Response):
    try:
        async with async_session_maker() as session:
            users_repo = UsersRepository(session)
            user = await users_repo.get_one_with_hashed_password(username=data.username)
            if user and AuthService().verify_password(data.password, user.password_hash):
                access_token = AuthService().create_access_token({'user_id':user.id})
                response.set_cookie(key="access_token", value=access_token)
                return {'access_token': access_token}
            raise HTTPException(
                status_code=401,
                detail='Authentication failed'
            )
    except DuplicateItemException:
        raise HTTPException(
            status_code=400,
            detail="User with these username, email or phone already exists",
        )
    

@router.get('/me', summary="Get Current User")
async def get_me(request: Request, user_id:UserIdDep):
    try:
        async with async_session_maker() as session:
            user = await UsersRepository(session).get_one_by_id(id=user_id)
            if user is None:
                raise HTTPException(
                    status_code=401,
                    detail='Could not validate credentials'
                )
            return user
    except (ItemNotFoundException):
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
@router.post('/logout', summary="Logout User")
async def logout_user(request: Request, response: Response, user_id:UserIdDep):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}
