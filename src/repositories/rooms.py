from datetime import date
from pydantic import BaseModel
from sqlalchemy import delete, insert, update
from sqlalchemy.exc import NoResultFound

from src.repositories.utils import rooms_ids_for_booking
from src.repositories.exceptions import ItemNotFoundException
from src.models.rooms import RoomsOrm
from src.schemas.rooms import (
    RoomsDbSchema,
    RoomsAddSchema,
    RoomsPatchDbSchema,
    RoomsPatchSchema,
    RoomsSchema,
)
from src.repositories.base import BaseRepository


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    scheme = RoomsSchema

    async def add(self, hotel_id: int, data: RoomsAddSchema) -> RoomsSchema:
        print(data)
        data = data.model_dump()
        data["hotel_id"] = hotel_id
        room = RoomsDbSchema.model_validate(data)
        stmt = insert(self.model).values(**room.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        return self.scheme.model_validate(result.scalars().one())

    async def edit(
        self,
        hotel_id: int,
        room_id: int,
        data: RoomsPatchSchema,
        exclude_unset: bool = False,
    ) -> BaseModel:
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
            return self.scheme.model_validate(result.scalars().one())
        except NoResultFound:
            raise ItemNotFoundException

    async def delete(self, hotel_id: int, room_id: int) -> None:
        stmt = delete(self.model).filter_by(hotel_id=hotel_id, id=room_id)
        result = await self.session.execute(stmt)
        if result.rowcount < 1:
            raise ItemNotFoundException

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        query = rooms_ids_for_booking(
            date_to=date_to, date_from=date_from, hotel_id=hotel_id
        )
        print(query)
        return await self.get_filtered(RoomsOrm.id.in_(query))
