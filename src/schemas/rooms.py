from pydantic import BaseModel, ConfigDict, Field


class RoomsAddSchema(BaseModel):
    title: str
    description: str | None
    price: int
    quantity: int

class RoomsAddDbSchema(RoomsAddSchema):
    hotel_id: int

class RoomsSchema(RoomsAddSchema):
    id: int
    hotel_id: int
    model_config = ConfigDict(from_attributes=True)


class RoomsPatchSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
