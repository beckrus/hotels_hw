from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies import DBDep, UserIdDep, get_admin_user
from src.services.auth import AuthService
from src.exceptions import ItemNotFoundException
from src.schemas.users import UserRequestUpdateSchema

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", dependencies=[Depends(get_admin_user)])
async def get_users(db: DBDep):  # Only admins
    users = await db.users.get_all()
    return {"status": "OK", "data": users}


@router.get(
    "/{user_id}", dependencies=[Depends(get_admin_user)]
)  # admin or the user itself
async def get_user_by_id(user_id: int, db: DBDep):
    try:
        user = await db.users.get_one_by_id(user_id)
        return user
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Item not found")


@router.patch("/{user_id}")  # admin or the user itself
async def update_user(
    user_id: int, data: UserRequestUpdateSchema, auth_user_id: UserIdDep, db: DBDep
):
    if auth_user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        user = await db.users.get_one_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="Item not found")
        if data.password:
            if data.password != data.password_confirm:
                raise HTTPException(status_code=400, detail="Passwords do not match")
            data.password = AuthService().hash_password(
                data.password.get_secret_value()
            )
        user = await db.users.edit(user_id, data, exclude_unset=True)
        await db.commit()
        return user
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Item not found")
