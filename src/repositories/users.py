from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select
from src.repositories.mappers.mappers import UsersDataMapper
from src.models.users import UsersOrm
from src.repositories.exceptions import DuplicateItemException
from src.schemas.users import UserHashedSchema, UserShowSchema
from src.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UsersDataMapper

    async def add(self, data: BaseModel) -> UserShowSchema:
        try:
            data.username = data.username.lower()
            stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            result = await self.session.execute(stmt)
            user_dict = result.scalars().one().__dict__
            user_dict.pop("password_hash")
            return self.mapper.map_to_domain_entity(user_dict)
        except IntegrityError as e:
            if e.orig.sqlstate == "23505":
                raise DuplicateItemException
            else:
                raise e

    async def get_one_with_hashed_password(self, username) -> UserHashedSchema:
        query = select(self.model).filter_by(username=username)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model:
            return UserHashedSchema.model_validate(
                {"id": model.id, "password_hash": model.password_hash}
            )
        return None
