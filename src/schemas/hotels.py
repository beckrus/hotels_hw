from pydantic import BaseModel


class HotelAddSchema(BaseModel):
    title: str
    location: str


class HotelSchema(HotelAddSchema):
    id: int


class HotelPatchSchema(BaseModel):
    title: str | None = None
    location: str | None = None
