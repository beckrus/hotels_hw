from typing import Type, TypeVar, Generic
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import NoResultFound

from src.repositories.exceptions import ItemNotFoundException, TooManyItemFoundException

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

    async def add(self, data: BaseModel):
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().one()

    async def edit(self, id: int, data: BaseModel):
        try:
            stmt = (
                update(self.model)
                .filter_by(id=id)
                .values(**data.model_dump())
                .returning(self.model)
            )
            # print(stmt.compile(compile_kwargs={"literal_binds": True}))  # debug
            result = await self.session.execute(stmt)
            return result.scalars().one()
        except NoResultFound:
            raise ItemNotFoundException

    # async def edit_by_filter(self, data: BaseModel, **filter_by):
    #     filter_by = {k: v for k, v in filter_by.items() if v is not None}
    #     try:
    #         stmt = (
    #             update(self.model)
    #             .filter_by(**filter_by)
    #             .values(**data.model_dump())
    #             .returning(self.model)
    #         )
    #         # print(stmt.compile(compile_kwargs={"literal_binds": True}))  # debug
    #         result = await self.session.execute(stmt)
    #         if result.rowcount < 1:
    #             raise ItemNotFoundException
    #         elif result.rowcount > 1:
    #             raise TooManyItemFoundException

    #         return result.scalars().one()
    #     except NoResultFound:
    #         raise ItemNotFoundException

    async def delete(self, id) -> None:
        stmt = delete(self.model).filter_by(id=id)
        # print(stmt.compile(compile_kwargs={"literal_binds": True}))  # debug
        result = await self.session.execute(stmt)
        if result.rowcount < 1:
            raise ItemNotFoundException

    # async def delete_by_filter(self, **filter_by) -> None:
    #     filter_by = {k: v for k, v in filter_by.items() if v is not None}
    #     stmt = delete(self.model).filter_by(**filter_by)
    #     # print(stmt.compile(compile_kwargs={"literal_binds": True}))  # debug
    #     result = await self.session.execute(stmt)
    #     if result.rowcount < 1:
    #         raise ItemNotFoundException
    #     elif result.rowcount > 1:
    #         raise TooManyItemFoundException

    async def commit(self):
        await self.session.commit()
