from datetime import date
from fastapi import APIRouter, Body, Depends, HTTPException, Query
# from fastapi_cache.decorator import cache

from src.repositories.exceptions import ItemNotFoundException
from src.api.dependencies import DBDep, PaginationDep, get_admin_user
from src.schemas.hotels import HotelAddSchema, HotelPatchSchema

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("")
# @cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(description="Title", default=None),
    location: str | None = Query(description="Location", default=None),
    date_from: date = Query(example="2025-03-24"),
    date_to: date = Query(example="2025-03-26"),
):
    return await db.hotels.get_filtered_by_time(
        location=location,
        title=title,
        limit=pagination.per_page,
        offset=(pagination.page - 1) * pagination.per_page,
        date_from=date_from,
        date_to=date_to,
    )


@router.get("/{id}")
# @cache(expire=10)
async def get_hotel_by_id(id: int, db: DBDep):
    try:
        return await db.hotels.get_one_by_id(id=id)
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/{hotel_id}", dependencies=[Depends(get_admin_user)])
async def delete_hotel(hotel_id: int, db: DBDep):
    try:
        await db.hotels.delete(id=hotel_id)
        await db.commit()
        return {"status": "OK"}
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Item not found")


@router.post("", dependencies=[Depends(get_admin_user)])
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAddSchema = Body(
        openapi_examples={
            "1": {
                "summary": "Hotel K",
                "value": {"title": "Hotel K", "location": "street K"},
            },
            "2": {
                "summary": "Hotel L",
                "value": {"title": "Hotel L", "location": "street L"},
            },
        }
    ),
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}


# patch, put
@router.patch("/{hotel_id}", dependencies=[Depends(get_admin_user)])
async def update_hotel(hotel_id: int, hotel_data: HotelPatchSchema, db: DBDep):
    try:
        hotel = await db.hotels.edit(hotel_id, hotel_data, exclude_unset=True)
        await db.commit()
        return {"status": "OK", "data": hotel}
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Item not found")


@router.put("/{hotel_id}", dependencies=[Depends(get_admin_user)])
async def rewrite_hotel(hotel_id: int, hotel_data: HotelAddSchema, db: DBDep):
    try:
        hotel = await db.hotels.edit(hotel_id, hotel_data)
        await db.commit()
        return {"status": "OK", "data": hotel}
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Item not found")
