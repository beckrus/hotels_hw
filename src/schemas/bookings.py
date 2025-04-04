from datetime import date
from pydantic import BaseModel, ConfigDict


class BookingsAddSchema(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingsDbAddSchema(BookingsAddSchema):
    id: int | None = None
    user_id: int
    price: int

    model_config = ConfigDict(from_attributes=True)


class BookingsSchema(BookingsDbAddSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
