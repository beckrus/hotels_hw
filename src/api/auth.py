from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from src.repositories.exceptions import DuplicateItemException, ItemNotFoundException
from src.repositories.users import UsersRepository
from src.schemas.users import UserAddSchema, UserHashedSchema
from src.database import async_session_maker
from src.config import settings

router = APIRouter(prefix="/users", tags=["auth"])

# import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


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
async def create_user(data: UserAddSchema):
    # if not admin set is_superuser to False and is_verified to False
    data.is_superuser = False
    data.is_varified = False
    if data.password != data.password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    if data.email is None and data.phone is None:
        raise HTTPException(status_code=400, detail="Email or phone is required")
    hashed_password = get_password_hash(data.password.get_secret_value())
    user_data = UserHashedSchema(**data.model_dump(), password_hash=hashed_password)

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


@router.put("/{user_id}")  # admin or the user itself
async def update_user(user_id: int, data: UserAddSchema):
    return {"message": f"Update user with id {user_id}"}
