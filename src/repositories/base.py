import logging
from typing import Type, TypeVar, Generic
from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.mappers.base import DataMapper
from src.exceptions import DuplicateItemException, ItemNotFoundException
from sqlalchemy.exc import IntegrityError

T = TypeVar("T")


class BaseRepository(Generic[T]):
    model: Type[T]
    mapper: DataMapper

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_filtered(self, *filter, **filter_by) -> list[BaseModel]:
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]

    async def get_all(self, *args, **kwargs) -> list[BaseModel]:
        return await self.get_filtered()

    async def get_one_or_none(self, **filters_by) -> BaseModel | None:
        query = select(self.model).filter_by(**filters_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def get_one_by_id(self, id: int) -> BaseModel:
        try:
            query = select(self.model).filter_by(id=id)
            result = await self.session.execute(query)
            data = result.scalars().one()
            return self.mapper.map_to_domain_entity(data)
        except NoResultFound:
            raise ItemNotFoundException

    async def add(self, data: BaseModel) -> None:
        try:
            stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            result = await self.session.execute(stmt)
            return self.mapper.map_to_domain_entity(result.scalars().one())
        except IntegrityError as e:
            logging.error(
                f"Can't add data in DB, error type: {type(e.orig.__cause__)=}, input data: {data}"
            )
            if e.orig.sqlstate == "23505":
                raise DuplicateItemException from e
            else:
                logging.critical(
                    f"Unknown error occurred, error type: {type(e.orig.__cause__)=}, input data: {data}, source: BaseRepository.add"
                )
                raise e

    async def add_bulk(self, data: list[BaseModel]) -> BaseModel:
        stmt = (
            insert(self.model)
            .values([item.model_dump() for item in data])
            .on_conflict_do_nothing()
        )
        await self.session.execute(stmt)

    async def edit(
        self, id: int, data: BaseModel, exclude_unset: bool = False
    ) -> BaseModel:
        try:
            stmt = (
                update(self.model)
                .filter_by(id=id)
                .values(**data.model_dump(exclude_unset=exclude_unset))
                .returning(self.model)
            )
            result = await self.session.execute(stmt)
            return self.mapper.map_to_domain_entity(result.scalars().one())
        except NoResultFound:
            raise ItemNotFoundException

    async def delete(self, id) -> None:
        stmt = delete(self.model).filter_by(id=id)
        result = await self.session.execute(stmt)
        if result.rowcount < 1:
            raise ItemNotFoundException

    async def delete_bulk(self, ids: list[int]) -> None:
        stmt = delete(self.model).filter(self.model.id.in_(ids))
        result = await self.session.execute(stmt)

        if result.rowcount < len(ids):
            raise ItemNotFoundException
