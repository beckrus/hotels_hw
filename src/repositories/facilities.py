from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.schemas.facilities import FacilitiesSchema, RoomsFacilitiesSchema
from src.repositories.base import BaseRepository


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    scheme = FacilitiesSchema


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    scheme = RoomsFacilitiesSchema
