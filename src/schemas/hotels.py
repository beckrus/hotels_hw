from pydantic import BaseModel, Field


class HotelSchema(BaseModel):
    title: str
    name: str


class HotelPatchSchema(BaseModel):
    title: str | None = Field(default=None)
    name: str | None = Field(default=None)
