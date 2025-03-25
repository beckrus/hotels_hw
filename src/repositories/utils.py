from datetime import date
from sqlalchemy import func, select

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm


def rooms_ids_for_booking(
    date_from: date,
    date_to: date,
    hotel_id: int | None = None,
):
    rooms_count = (
        select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
        .filter(
            BookingsOrm.date_from <= date_to,
            BookingsOrm.date_to >= date_from,
        )
        .group_by(BookingsOrm.room_id)
        .cte(name="rooms_count")
    )
    rooms_left = (
        select(
            RoomsOrm.id.label("room_id"),
            (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label(
                "rooms_left"
            ),
        )
        .select_from(RoomsOrm)
        .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
    )
    if hotel_id:
        rooms_left = rooms_left.filter(RoomsOrm.hotel_id == hotel_id)
    rooms_left = rooms_left.cte(name="rooms_left")
    rooms_ids_query = (
        select(rooms_left.c.room_id)
        .select_from(rooms_left)
        .where(rooms_left.c.rooms_left > 0)
    )
    return rooms_ids_query
