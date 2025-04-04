from src.api.dependencies import get_db_manager_null_pull
from src.schemas.hotels import HotelAddSchema


async def test_add_hotel():
    hotel_data = HotelAddSchema(title="Hotel A", location="Moscow, First street 1a")
    async with get_db_manager_null_pull() as db:
        new_hotel_data = await db.hotels.add(hotel_data)
        await db.commit()
