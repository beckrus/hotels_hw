from src.schemas.bookings import BookingsAddSchema
from src.exceptions import (
    BookingNotFoundException,
    ItemNotFoundException,
    RoomNotFoundException,
)
from src.services.base import BaseService


class BookingsService(BaseService):
    async def get_all_bookings(self) -> list:
        return await self.db.bookings.get_all()

    async def get_users_bookings(self, user_id: int) -> list:
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def get_booking(self, id: int, user_id: int) -> dict:
        return await self.db.bookings.get_filtered(id=id, user_id=user_id)

    async def add_booking(self, user_id: int, data: BookingsAddSchema):
        try:
            room = await self.db.rooms.get_one_by_id(id=data.room_id)
        except ItemNotFoundException as e:
            raise RoomNotFoundException from e
        room_price = room.price * (data.date_to - data.date_from).days
        booking = await self.db.bookings.add_booking(
            user_id=user_id, price=room_price, data=data
        )
        await self.db.commit()
        return booking

    async def delete_booking(self, booking_id: int, user_id: int) -> None:
        booking = await self.db.bookings.get_filtered(id=booking_id, user_id=user_id)
        if not booking:
            raise BookingNotFoundException
        await self.db.bookings.delete(id=booking_id)
        await self.db.commit()
