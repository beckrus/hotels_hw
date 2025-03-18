from fastapi import APIRouter, Body, HTTPException, Query
from schemas.hotels import HotelPatchSchema, HotelSchema


hotels: list[dict[str, str | int]] = [
    {"id": 1, "title": "Hotel A", "name": "A"},
    {"id": 2, "title": "Hotel B", "name": "B"},
    {"id": 3, "title": "Hotel C", "name": "C"},
    {"id": 4, "title": "Hotel D", "name": "D"},
    {"id": 5, "title": "Hotel E", "name": "E"},
    {"id": 6, "title": "Hotel F", "name": "F"},
    {"id": 7, "title": "Hotel G", "name": "G"},
    {"id": 8, "title": "Hotel H", "name": "H"},
    {"id": 9, "title": "Hotel I", "name": "I"},
    {"id": 10, "title": "Hotel J", "name": "J"},
]


router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("")
def get_hotels(
    title: str | None = Query(description="Title", default=None),
    id: int | None = Query(description="id", default=None),
    page: int = Query(description="Page", default=1, ge=1),
    per_page: int = Query(description="Limit", default=3, ge=1, lt=101),
):
    start_hotel = (page - 1) * per_page
    _hotels = []
    if title or id:
        for h in hotels:
            if title and title == h["title"]:
                _hotels.append(h)
            if id and id == h["id"]:
                _hotels.append(h)
    else:
        _hotels = list(hotels)
    if start_hotel >= len(_hotels):
        raise HTTPException(status_code=416)
    return _hotels[start_hotel:per_page]


@router.delete("/{hotel_id}")
def delete_hotel(
    hotel_id: int,
):
    for h in hotels:
        if hotel_id == h["id"]:
            hotels.remove(h)
            return {"status": "Ok"}
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("")
def create_hotel(
    hotel_data: HotelSchema = Body(
        openapi_examples={
            "1": {"summary": "Hotel K", "value": {"title": "Hotel K", "name": "K"}},
            "2": {"summary": "Hotel L", "value": {"title": "Hotel L", "name": "L"}},
        }
    ),
):
    id = int(hotels[-1]["id"]) + 1
    hotels.append({"id": id, "title": hotel_data.title, "name": hotel_data.name})
    return hotels[-1]


# patch, put
@router.patch("/{hotel_id}")
def update_hotel(hotel_id: int, hotel_data: HotelPatchSchema):
    for h in hotels:
        if hotel_id == h["id"]:
            if hotel_data.title:
                h["title"] = hotel_data.title
            if hotel_data.name:
                h["name"] = hotel_data.name
            return h
    raise HTTPException(status_code=404, detail="Item not found")


@router.put("/{hotel_id}")
def rewrite_hotel(
    hotel_id: int,
    hotel_data: HotelSchema,
):
    for h in hotels:
        if hotel_id == h["id"]:
            h["title"] = hotel_data.title
            h["name"] = hotel_data.name
            return h
    raise HTTPException(status_code=404, detail="Item not found")
