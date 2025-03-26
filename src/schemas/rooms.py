from pydantic import BaseModel, ConfigDict, Field

from src.schemas.facilities import FacilitiesSchema


class RoomsAddSchema(BaseModel):
    title: str
    description: str | None
    price: int
    quantity: int
    facilities: list[int] | None = None


class RoomsAddDBSchema(BaseModel):
    title: str
    description: str | None
    price: int
    quantity: int


class RoomsDbSchema(RoomsAddDBSchema):
    hotel_id: int


class RoomsSchema(RoomsAddSchema):
    id: int
    hotel_id: int

    model_config = ConfigDict(from_attributes=True)

class RoomsWithRel(RoomsSchema):
    facilities: list[FacilitiesSchema]

class RoomsPatchSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities: list[int] = []


class RoomsPatchDbSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None

class RoomsPutSchema(BaseModel):
    title: str
    description: str
    price: int
    quantity: int
    facilities: list[int]