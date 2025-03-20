from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert
from src.models.users import UsersOrm
from src.repositories.exceptions import DuplicateItemException
from src.schemas.users import UserShowSchema
from src.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UsersOrm
    scheme = UserShowSchema

    async def add(self, data: BaseModel) -> UserShowSchema:
        try:
            stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            result = await self.session.execute(stmt)
            user_dict = result.scalars().one().__dict__
            user_dict.pop("password_hash")
            return self.scheme.model_validate(user_dict)
        except IntegrityError as e:
            if e.orig.sqlstate == "23505":
                raise DuplicateItemException
            else:
                raise e
