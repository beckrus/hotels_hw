from datetime import date
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.orm import selectinload, joinedload

from src.repositories.mappers.mappers import RoomsDataMapper, RoomsWithRelDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.repositories.exceptions import ItemNotFoundException, FKNotFoundException
from src.models.rooms import RoomsOrm
from src.schemas.rooms import (
    RoomsDbSchema,
    RoomsAddSchema,
    RoomsPatchDbSchema,
    RoomsPatchSchema,
    RoomsSchema,
    RoomsWithRel,
)
from src.repositories.base import BaseRepository


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomsDataMapper

    async def add(self, hotel_id: int, data: RoomsAddSchema) -> RoomsSchema:
        data = data.model_dump()
        data["hotel_id"] = hotel_id
        room = RoomsDbSchema.model_validate(data)
        stmt = insert(self.model).values(**room.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(stmt)
            return self.mapper.map_to_domain_entity(result.scalars().one())
        except IntegrityError as e:
            if e.orig.sqlstate == 23503:
                raise FKNotFoundException
            else:
                raise e

    async def edit(
        self,
        hotel_id: int,
        room_id: int,
        data: RoomsPatchSchema,
        exclude_unset: bool = False,
    ) -> RoomsSchema:
        room = RoomsPatchDbSchema.model_validate(
            data.model_dump(exclude_unset=exclude_unset)
        )
        if not bool(room.model_dump(exclude_unset=exclude_unset)):
            return await self.get_one_by_id(id=room_id)
        try:
            stmt = (
                update(self.model)
                .filter_by(hotel_id=hotel_id, id=room_id)
                .values(**room.model_dump(exclude_unset=exclude_unset))
                .returning(self.model)
            )
            result = await self.session.execute(stmt)
            return self.mapper.map_to_domain_entity(result.scalars().one())
        except NoResultFound:
            raise ItemNotFoundException

    async def delete(self, hotel_id: int, room_id: int) -> None:
        stmt = delete(self.model).filter_by(hotel_id=hotel_id, id=room_id)
        result = await self.session.execute(stmt)
        if result.rowcount < 1:
            raise ItemNotFoundException

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        rooms_ids = rooms_ids_for_booking(
            date_to=date_to, date_from=date_from, hotel_id=hotel_id
        )
        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(self.model.id.in_(rooms_ids))
        )
        result = await self.session.execute(query)
        return [
            RoomsWithRelDataMapper.map_to_domain_entity(model)
            for model in result.unique().scalars().all()
        ]

    async def get_one_by_id_with_rel(self, hotel_id: int, id: int) -> RoomsWithRel:
        try:
            query = (
                select(self.model)
                .options(selectinload(self.model.facilities))
                .filter_by(hotel_id=hotel_id, id=id)
            )
            result = await self.session.execute(query)
            return RoomsWithRelDataMapper.map_to_domain_entity(result.scalars().one())
        except NoResultFound:
            raise ItemNotFoundException
