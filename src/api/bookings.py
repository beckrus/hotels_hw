from fastapi import APIRouter, Depends, HTTPException, Request

from repositories.exceptions import ItemNotFoundException
from src.schemas.bookings import BookingsAddSchema
from src.api.dependencies import DBDep, UserIdDep


router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("/")
async def get_users_bookings(
    request: Request, 
    db: DBDep, 
    user_id:UserIdDep):

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
    user_id:UserIdDep,
):
    try:
        res_room = await db.rooms.get_one_by_id(id=data.room_id)
        quantity = res_room.quantity
        # await db.bookings.get_filtered(
        #     room_id=data.room_id, 
        #     date_from=data.date_from, 
        #     date_to=data.date_to
        # ) #add filter for avaialbility
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Room not found")
    price = res_room.price * (data.date_to - data.date_from).days
    booking = await db.bookings.add(user_id=user_id, price=price,data=data)
    await db.commit()
    return {"status": "OK", "data": booking}
