from datetime import date
from schemas.facilities import RoomsFacilitiesAddSchema
from src.schemas.rooms import RoomsPatchSchema
from src.services.base import BaseService


class RoomsService(BaseService):
    async def get_hotel_rooms(self, hotel_id: int, date_from: date, date_to: date):
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

    async def get_room_by_id(self, hotel_id: int, room_id: int):
        return await self.db.rooms.get_one_by_id_with_rel(hotel_id=hotel_id, id=room_id)

    async def create_room(self, hotel_id, data):
        room = await self.db.rooms.add(hotel_id=hotel_id, data=data)
        await self.db.commit()
        return room

    async def update_room(self, hotel_id: int, room_id: int, data: RoomsPatchSchema):
        room = await self.db.rooms.edit(
            hotel_id=hotel_id, room_id=room_id, data=data, exclude_unset=True
        )
        room_facilities_add = [
            RoomsFacilitiesAddSchema.model_validate(
                {"room_id": room.id, "facility_id": n}
            )
            for n in data.facilities
        ]
        await self.db.rooms_facilities.add_bulk(room_facilities_add)
        await self.db.commit()
        return room

    async def rewrite_room(self, hotel_id: int, room_id: int, data: RoomsPatchSchema):
        room = await self.db.rooms.edit(
            hotel_id=hotel_id, room_id=room_id, data=data, exclude_unset=True
        )
        room_facilities = await self.db.rooms_facilities.get_filtered(room_id=room_id)
        room_facilities_delete = [
            n.id for n in room_facilities if n.facility_id not in data.facilities
        ]
        room_facilities_add = [
            RoomsFacilitiesAddSchema.model_validate(
                {"room_id": room.id, "facility_id": n}
            )
            for n in data.facilities
            if n not in [f.facility_id for f in room_facilities]
        ]
        if room_facilities_delete:
            await self.db.rooms_facilities.delete_bulk(room_facilities_delete)
        if room_facilities_add:
            await self.db.rooms_facilities.add_bulk(room_facilities_add)
        await self.db.commit()

        return room

    async def delete_room(self, room_id: int):
        await self.db.rooms.delete(id=room_id)
        await self.db.commit()
