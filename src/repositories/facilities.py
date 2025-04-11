from asyncpg import ForeignKeyViolationError
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from src.exceptions import FacilityNotFoundException, RoomNotFoundException
from src.schemas.facilities import RoomsFacilitiesSchema
from src.repositories.mappers.mappers import (
    FacilitiesDataMapper,
    RoomsFacilitiesDataMapper,
)
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilitiesDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    mapper = RoomsFacilitiesDataMapper

    async def add_bulk(self, data: list[RoomsFacilitiesSchema]) -> None:
        try:
            stmt = (
                insert(self.model)
                .values([item.model_dump() for item in data])
                .on_conflict_do_nothing()
            )
            await self.session.execute(stmt)
        except IntegrityError as e:
            if isinstance(e.orig.__cause__, ForeignKeyViolationError):
                if "rooms_facilities_facility_id_fkey" in str(e.orig):
                    raise FacilityNotFoundException from e
                else:
                    raise RoomNotFoundException from e
