from src.schemas.hotels import HotelAddSchema


async def test_add_hotel(db):
    hotel_data = HotelAddSchema(title="Hotel A", location="Moscow, First street 1a")
    await db.hotels.add(hotel_data)
    await db.commit()
