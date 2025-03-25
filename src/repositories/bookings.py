from sqlalchemy import insert
from src.models.bookings import BookingsOrm
from src.schemas.bookings import BookingsAddSchema, BookingsDbAddSchema, BookingsSchema
from src.repositories.base import BaseRepository


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    scheme = BookingsSchema

    async def add(
        self, price: int, user_id: int, data: BookingsAddSchema
    ) -> BookingsSchema:
        booking = BookingsDbAddSchema(user_id=user_id, price=price, **data.model_dump())
        stmt = insert(self.model).values(**booking.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        return self.scheme.model_validate(result.scalars().one())
