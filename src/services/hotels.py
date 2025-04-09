from datetime import date
from api.dependencies import PaginationDep
from src.services.base import BaseService


class HotelsService(BaseService):
    async def get_hotels(
        self,
        pagination: PaginationDep,
        title: str | None,
        location: str | None,
        date_from: date,
        date_to: date,
    ):
        return await self.db.hotels.get_filtered_by_time(
            location=location,
            title=title,
            limit=pagination.per_page,
            offset=(pagination.page - 1) * pagination.per_page,
            date_from=date_from,
            date_to=date_to,
        )

    async def get_hotel_by_id(self, id: int):
        return await self.db.hotels.get_one_by_id(id=id)

    async def create_hotel(self, hotel_data):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def update_hotel(self, hotel_id: int, hotel_data):
        hotel = await self.db.hotels.edit(hotel_id, hotel_data, exclude_unset=True)
        await self.db.commit()
        return hotel

    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()
