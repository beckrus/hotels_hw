from src.models.facilities import FacilitiesOrm
from src.schemas.facilities import FacilitiesSchema
from src.repositories.base import BaseRepository


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    scheme = FacilitiesSchema