from sqlalchemy import func, select
from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
        self,
        offset: int,
        limit: int,
        location: str | None = None,
        title: str | None = None,
    ):
        query = select(self.model)
        if location:
            query = query.where(
                func.lower(HotelsOrm.location).contains(location.strip().lower())
            )
        if title:
            query = query.where(
                func.lower(HotelsOrm.title).contains(title.strip().lower())
            )
        query = query.limit(limit).offset(offset)
        # print(query.compile(compile_kwargs={"literal_binds": True}))  # debug
        result = await self.session.execute(query)
        hotels = result.scalars().all()
        return hotels
