
from fastapi import APIRouter, HTTPException

from src.api.dependencies import UserIdAdminDep, UserIdDep
from src.services.auth import AuthService
from src.repositories.exceptions import ItemNotFoundException
from src.repositories.users import UsersRepository
from src.schemas.users import  UserRequestUpdateSchema
from src.database import async_session_maker

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("")
async def get_users(auth_user_id: UserIdAdminDep):  # Only admins
    async with async_session_maker() as session:
        users_repo = UsersRepository(session)
        users = await users_repo.get_all()
        return users
    return {"status": "OK", "data": users}


@router.get("/{user_id}")  # admin or the user itself
async def get_user_by_id(user_id: int, auth_user_id: UserIdAdminDep):
    try:
        async with async_session_maker() as session:
            users_repo = UsersRepository(session)
            user = await users_repo.get_one_by_id(user_id)
            return user
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Item not found")
    

@router.patch("/{user_id}")  # admin or the user itself
async def update_user(user_id: int, data: UserRequestUpdateSchema, auth_user_id: UserIdDep):
    if auth_user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        async with async_session_maker() as session:
            users_repo = UsersRepository(session)
            user = await users_repo.get_one_by_id(user_id)
            if user is None:
                raise HTTPException(status_code=404, detail="Item not found")
            if data.password:
                if data.password != data.password_confirm:
                    raise HTTPException(status_code=400, detail="Passwords do not match")
                data.password = AuthService().hash_password(data.password.get_secret_value())
            user = await users_repo.edit(user_id, data, exclude_unset=True)
            await users_repo.commit()
            return user
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": f"Update user with id {user_id}"}