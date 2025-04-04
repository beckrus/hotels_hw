from datetime import date, timedelta
from src.schemas.bookings import BookingsAddSchema
from utils.db_manager import DBManager


async def test_booking_crud(db:DBManager):
    user = (await db.users.get_all())[0].id
    room = (await db.rooms.get_all())[0].id
    hotel_data = BookingsAddSchema(
        room_id = room,
        date_from = date.today(),
        date_to = date.today() + timedelta(days=10),
    )
    booking_added = await db.bookings.add(user_id=user, price=1000, data=hotel_data)
    assert booking_added

    booking_get = await db.bookings.get_one_or_none(id=booking_added.id)
    assert booking_get

    hotel_data.date_to = date.today() + timedelta(days=5)
    booking_updated = await db.bookings.edit(
        booking_get.id, 
        hotel_data)
    assert booking_updated.date_to == hotel_data.date_to

    await db.bookings.delete(booking_get.id)
    await db.commit()

    booking_get_after_del = await db.bookings.get_one_or_none(id=booking_added.id)
    assert not booking_get_after_del

