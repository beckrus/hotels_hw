from datetime import date
from sqlalchemy import insert, select

from src.repositories.mappers.mappers import BookingsDataMapper
from src.models.bookings import BookingsOrm
from src.schemas.bookings import BookingsAddSchema, BookingsSchema
from src.repositories.base import BaseRepository


class BookingsRepository(BaseRepository):
    model: BookingsOrm = BookingsOrm
    mapper: BookingsDataMapper = BookingsDataMapper

    async def add(
        self, price: int, user_id: int, data: BookingsAddSchema
    ) -> BookingsSchema:
        booking = {**data.model_dump(), "user_id": user_id, "price": price}
        stmt = insert(self.model).values(**booking).returning(self.model)
        result = await self.session.execute(stmt)
        return self.mapper.map_to_domain_entity(result.scalars().one())

    async def get_bookings_with_today_checkin(self):
        query = select(self.model).filter(self.model.date_from == date.today())
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(n) for n in result.scalars().all()]
