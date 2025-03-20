
from fastapi import APIRouter, HTTPException, Response, Request

from src.services.exceptions import InvalidTokenDataError
from src.services.auth import AuthService
from src.repositories.exceptions import DuplicateItemException, ItemNotFoundException
from src.repositories.users import UsersRepository
from src.schemas.users import UserHashedPwdAddSchema, UserLoginSchema, UserRequestAddSchema
from src.database import async_session_maker

router = APIRouter(prefix="/users", tags=["auth"])



# def authenticate_user(fake_db, username: str, password: str):
#     user = get_user(fake_db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user

@router.get("")
async def get_users():  # Only admins
    async with async_session_maker() as session:
        users_repo = UsersRepository(session)
        users = await users_repo.get_all()
        return users
    return {"status": "OK", "data": users}


@router.get("/{user_id}")  # admin or the user itself
async def get_user_by_id(user_id: int):
    try:
        async with async_session_maker() as session:
            users_repo = UsersRepository(session)
            user = await users_repo.get_one_by_id(user_id)
            return user
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Item not found")


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
async def create_user(data: UserLoginSchema, response: Response):
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
    
@router.put("/{user_id}")  # admin or the user itself
async def update_user(user_id: int, data: UserRequestAddSchema):
    return {"message": f"Update user with id {user_id}"}

@router.get('/me/')
async def get_me(request: Request):
    access_token = request.cookies.get('access_token')
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail='Not authenticated'
        )
    try:
        user_id = AuthService().get_current_user(access_token)
        async with async_session_maker() as session:
            user = await UsersRepository(session).get_one_by_id(id=user_id)
            if user is None:
                raise HTTPException(
                    status_code=401,
                    detail='Could not validate credentials'
                )
            return user
    except (ItemNotFoundException, InvalidTokenDataError):
        raise HTTPException(status_code=401, detail="Could not validate credentials")