from pydantic import BaseModel, ConfigDict


class FacilitiesAddSchema(BaseModel):
    name: str


class FacilitiesSchema(FacilitiesAddSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomsFacilitiesAddSchema(BaseModel):
    room_id: int
    facility_id: int


class RoomsFacilitiesSchema(RoomsFacilitiesAddSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
