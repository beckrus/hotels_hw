from typing import Type, TypeVar, Generic
from sqlalchemy import insert, select, update
from sqlalchemy.exc import NoResultFound

from src.repositories.exceptions import ItemNotFoundException

T = TypeVar("T")


class BaseRepository(Generic[T]):  # noqa: F821
    model: Type[T]

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        # print(query.compile(compile_kwargs={"literal_binds": True}))  # debug
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filters_by):
        query = select().filter_by(**filters_by).returning(self.model)
        # print(query.compile(compile_kwargs={"literal_binds": True}))  # debug
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, **kwargs):
        stmt = insert(self.model).values(**kwargs).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().one()

    async def update(self, id, **kwargs):
        try:
            stmt = (
                update(self.model)
                .filter_by(id=id)
                .values(**kwargs)
                .returning(self.model)
            )
            # print(stmt.compile(compile_kwargs={"literal_binds": True}))  # debug
            result = await self.session.execute(stmt)
            return result.scalars().one()
        except NoResultFound:
            raise ItemNotFoundException

    async def commit(self):
        await self.session.commit()
