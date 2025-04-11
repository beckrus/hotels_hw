from src.exceptions import (
    DuplicateItemException,
    FacilityDuplicateException,
    FacilityNotFoundException,
    ItemNotFoundException,
)
from schemas.facilities import FacilitiesAddSchema
from src.services.base import BaseService


class FacilitiesService(BaseService):
    async def get_facilities(self, name: str | None = None):
        filter = {"name": name} if name else {}

        return await self.db.facilities.get_filtered(**filter)

    async def get_facility_by_id(self, facility_id: int):
        try:
            return await self.db.facilities.get_one_by_id(id=facility_id)
        except ItemNotFoundException as e:
            raise FacilityNotFoundException from e

    async def create_facility(self, data):
        try:
            facility = await self.db.facilities.add(data)
            await self.db.commit()
            return {"status": "OK", "data": facility}
        except DuplicateItemException as e:
            raise FacilityDuplicateException from e

    async def update_facility(self, facility_id: int, data: FacilitiesAddSchema):
        try:
            facility = await self.db.facilities.edit(facility_id, data)
            await self.db.commit()
            return facility
        except ItemNotFoundException as e:
            raise FacilityNotFoundException from e

    async def delete(self, id: int):
        try:
            await self.db.facilities.delete(id=id)
            await self.db.commit()
        except ItemNotFoundException as e:
            raise FacilityNotFoundException from e
