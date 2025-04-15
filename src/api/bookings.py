from fastapi import APIRouter, Depends

from src.exceptions import (
    BookingNotFoundException,
    BookingNotFoundHttpException,
    NoRoomAvailableException,
    NoRoomAvailableHttpException,
    RoomNotFoundException,
    RoomNotFoundHttpException,
)
from src.services.bookings import BookingsService
from src.schemas.bookings import BookingsAddSchema
from src.api.dependencies import DBDep, UserIdDep, get_current_user


router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("/", dependencies=[Depends(get_current_user)])
async def get_all_bookings(db: DBDep):
    bookings = await BookingsService(db).get_all_bookings()
    return {"status": "OK", "data": bookings}


@router.get("/me")
async def get_users_bookings(db: DBDep, user_id: UserIdDep):
    bookings = await BookingsService(db).get_users_bookings(user_id)
    return {"status": "OK", "data": bookings}


@router.get("/{booking_id}")
async def get_booking(
    db: DBDep,
    booking_id: int,
    user_id: UserIdDep,
):
    booking = await BookingsService(db).get_booking(id=booking_id, user_id=user_id)
    return {"status": "OK", "data": booking}


@router.post("/")
async def add_booking(
    db: DBDep,
    data: BookingsAddSchema,
    user_id: UserIdDep,
):
    try:
        booking = await BookingsService(db).add_booking(user_id, data)
        return {"status": "OK", "data": booking}
    except RoomNotFoundException as e:
        raise RoomNotFoundHttpException from e
    except NoRoomAvailableException:
        raise NoRoomAvailableHttpException


@router.delete("/{booking_id}")
async def delete_booking(
    db: DBDep,
    booking_id: int,
    user_id: UserIdDep,
):
    try:
        await BookingsService(db).delete_booking(booking_id, user_id)
        return {"status": "OK"}
    except BookingNotFoundException:
        raise BookingNotFoundHttpException
