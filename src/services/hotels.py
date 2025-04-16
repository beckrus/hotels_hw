from datetime import date
from src.api.dependencies import PaginationDep
from src.exceptions import (
    DuplicateItemException,
    HotelDumpicateHttpException,
    HotelNotFoundException,
    ItemNotFoundException,
)
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
        try:
            return await self.db.hotels.get_one_by_id(id=id)
        except ItemNotFoundException as e:
            raise HotelNotFoundException from e

    async def create_hotel(self, hotel_data):
        try:
            hotel = await self.db.hotels.add(hotel_data)
            await self.db.commit()
            return hotel
        except DuplicateItemException:
            raise HotelDumpicateHttpException

    async def update_hotel(self, hotel_id: int, hotel_data):
        try:
            hotel = await self.db.hotels.edit(hotel_id, hotel_data, exclude_unset=True)
            await self.db.commit()
            return hotel
        except ItemNotFoundException as e:
            raise HotelNotFoundException from e

    async def delete_hotel(self, hotel_id: int):
        try:
            await self.db.hotels.delete(id=hotel_id)
            await self.db.commit()
        except ItemNotFoundException as e:
            raise HotelNotFoundException from e
