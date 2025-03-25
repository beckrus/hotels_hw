from fastapi import APIRouter, HTTPException, Request

from repositories.exceptions import ItemNotFoundException
from src.schemas.bookings import BookingsAddSchema
from src.api.dependencies import DBDep, UserIdDep, UserIdAdminDep


router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("/")
async def get_all_bookings(request: Request, db: DBDep, user_id: UserIdAdminDep):
    bookings = await db.bookings.get_all()
    return {"status": "OK", "data": bookings}


@router.get("/me")
async def get_users_bookings(request: Request, db: DBDep, user_id: UserIdDep):
    bookings = await db.bookings.get_filtered(user_id=user_id)
    return {"status": "OK", "data": bookings}


@router.get("/{booking_id}")
async def get_booking(
    request: Request,
    db: DBDep,
    booking_id: int,
    user_id: UserIdDep,
):
    booking = await db.bookings.get_filtered(id=booking_id, user_id=user_id)
    return {"status": "OK", "data": booking}


@router.post("/")
async def add_booking(
    request: Request,
    db: DBDep,
    data: BookingsAddSchema,
    user_id: UserIdDep,
):
    try:
        room = await db.rooms.get_one_by_id(id=data.room_id)
        # add filter for avaialbility
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Room not found")
    room_price = room.price * (data.date_to - data.date_from).days
    booking = await db.bookings.add(user_id=user_id, price=room_price, data=data)
    await db.commit()
    return {"status": "OK", "data": booking}


@router.delete("/{booking_id}")
async def delete_booking(
    request: Request,
    db: DBDep,
    booking_id: int,
    user_id: UserIdDep,
):
    try:
        booking = await db.bookings.get_filtered(id=booking_id, user_id=user_id)
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Item not found")
    await db.bookings.delete(booking_id=booking.id)
    await db.commit()
    return {"status": "OK"}
