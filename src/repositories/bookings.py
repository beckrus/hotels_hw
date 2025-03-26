from sqlalchemy import insert
from repositories.mappers.mappers import BookingsDataMapper
from src.models.bookings import BookingsOrm
from src.schemas.bookings import BookingsAddSchema, BookingsSchema
from src.repositories.base import BaseRepository


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingsDataMapper

    async def add(
        self, price: int, user_id: int, data: BookingsAddSchema
    ) -> BookingsSchema:
        data = {**data.model_dump(), "user_id": user_id, "price": price}
        booking = self.mapper.map_to_persistence_entity(data)
        stmt = insert(self.model).values(**booking.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)

        return self.mapper.map_to_domain_entity(result.scalars().one())
