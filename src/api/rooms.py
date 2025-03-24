from fastapi import APIRouter, Body, HTTPException

from src.api.dependencies import DBDep
from src.repositories.exceptions import ItemNotFoundException
from src.schemas.rooms import RoomsAddSchema, RoomsPatchSchema

router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get("/{hotel_id}/rooms")
async def get_hotel_rooms(hotel_id: int, db: DBDep):
    rooms = await db.rooms.get_filtered(hotel_id=hotel_id)
    return {"status": "OK", "data": rooms}


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_hotel_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        room = await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)
        return {"status": "OK", "data": room}
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Item not found")


@router.post("/{hotel_id}/rooms")
async def add_hotel_room(
    db: DBDep,
    hotel_id: int,
    data: RoomsAddSchema = Body(
        openapi_examples={
            "1": {
                "summary": "Luxury",
                "value": {
                    "title": "Luxury",
                    "description": "Indulge in the ultimate luxury experience in our exquisitely designed suite. This spacious room features a king-sized bed with plush, high-thread-count linens, a separate living area with elegant furnishings, and a private balcony offering stunning panoramic views of the city. The room is equipped with modern amenities, including a 55-inch flat-screen TV, high-speed Wi-Fi, and a Nespresso coffee machine for your convenience",
                    "price": 500,
                    "quantity": 9,
                },
            },
            "2": {
                "summary": "Deluxe",
                "value": {
                    "title": "Deluxe",
                    "description": "Our Deluxe Room offers a perfect blend of comfort and elegance. Featuring a queen-sized bed with premium linens, a cozy seating area, and large windows that provide plenty of natural light, this room is designed to make you feel at home. Modern amenities include a 42-inch flat-screen TV, high-speed Wi-Fi, and a minibar. The en-suite bathroom is equipped with a walk-in shower, plush towels, and complimentary toiletries. Ideal for both business and leisure travelers, our Deluxe Room ensures a pleasant and relaxing stay.",
                    "price": 300,
                    "quantity": 10,
                },
            },
            "3": {
                "summary": "Standart",
                "value": {
                    "title": "Standart",
                    "description": "Our Standard Room is designed for comfort and convenience. It features a comfortable double bed, a work desk, and a flat-screen TV. The room is equipped with high-speed Wi-Fi, air conditioning, and a coffee maker. The private bathroom includes a shower, fresh towels, and basic toiletries. Perfect for short stays, our Standard Room offers all the essentials you need for a comfortable visit.",
                    "price": 150,
                    "quantity": 20,
                },
            },
        }
    ),
):
    room = await db.rooms.add(hotel_id=hotel_id, data=data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def edit_hotel_room(
    hotel_id: int, room_id: int, data: RoomsPatchSchema, db: DBDep
):
    try:
        room = await db.rooms.edit(hotel_id=hotel_id, room_id=room_id, data=data)
        await db.commit()
        return {"status": "OK", "data": room}
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/{hotel_id}/rooms/{room_id}")
async def del_hotel_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        await db.rooms.delete(
            hotel_id=hotel_id,
            room_id=room_id,
        )
        await db.commit()
        return {"status": "OK"}
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Item not found")
