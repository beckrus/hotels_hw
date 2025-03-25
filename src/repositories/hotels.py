from datetime import date
from sqlalchemy import func, select

from src.models.rooms import RoomsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import HotelSchema
from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    scheme = HotelSchema

    async def get_all(
        self,
        offset: int,
        limit: int,
        location: str | None = None,
        title: str | None = None,
    ) -> list[HotelSchema]:
        query = select(self.model)
        if location:
            query = query.where(
                func.lower(self.model.location).contains(location.strip().lower())
            )
        if title:
            query = query.where(
                func.lower(self.model.title).contains(title.strip().lower())
            )
        query = query.limit(limit).offset(offset)
        # print(query.compile(compile_kwargs={"literal_binds": True}))  # debug
        result = await self.session.execute(query)
        hotels = [
            self.scheme.model_validate(hotel, from_attributes=True)
            for hotel in result.scalars().all()
        ]
        return hotels
    
    async def get_filtered_by_time(
            self, 
            date_from:date, 
            date_to:date,
            offset: int,
            limit: int,
            location: str | None = None,
            title: str | None = None
    ):
        rooms_ids = rooms_ids_for_booking(date_to=date_to,
                                      date_from=date_from)
        hotels_ids = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids))
        )
        query = (select(HotelsOrm)
                 .filter((HotelsOrm.id.in_(hotels_ids)))

        )
        if location:
            query = query.where(
                func.lower(self.model.location).contains(location.strip().lower())
            )
        if title:
            query = query.where(
                func.lower(self.model.title).contains(title.strip().lower())
            )

        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        hotels = [
            self.scheme.model_validate(hotel, from_attributes=True)
            for hotel in result.scalars().all()
        ]
        return hotels