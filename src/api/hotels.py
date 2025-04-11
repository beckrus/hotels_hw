from datetime import date
from fastapi import APIRouter, Body, Depends, HTTPException, Query
from fastapi_cache.decorator import cache

from src.services.hotels import HotelsService
from src.exceptions import (
    HotelNotFoundException,
    HotelNotFoundHttpException,
)
from src.api.dependencies import DBDep, PaginationDep, get_admin_user
from src.schemas.hotels import HotelAddSchema, HotelPatchSchema, HotelSchema

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("", response_model=list[HotelSchema])
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(description="Title", default=None),
    location: str | None = Query(description="Location", default=None),
    date_from: date = Query(example="2025-03-24"),
    date_to: date = Query(example="2025-03-26"),
):
    if date_from > date_to:
        raise HTTPException(status_code=422, detail="date from > date to")
    return await HotelsService(db).get_hotels(
        pagination, title, location, date_from, date_to
    )


@router.get("/{id}")
@cache(expire=10)
async def get_hotel_by_id(id: int, db: DBDep):
    try:
        return await HotelsService(db).get_hotel_by_id(id)
    except HotelNotFoundException:
        raise HotelNotFoundHttpException


@router.delete("/{hotel_id}", dependencies=[Depends(get_admin_user)])
async def delete_hotel(hotel_id: int, db: DBDep):
    try:
        await HotelsService(db).delete_hotel(hotel_id)
        return {"status": "OK"}
    except HotelNotFoundException:
        raise HotelNotFoundHttpException


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
    hotel = await HotelsService(db).create_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.patch("/{hotel_id}", dependencies=[Depends(get_admin_user)])
async def update_hotel(hotel_id: int, hotel_data: HotelPatchSchema, db: DBDep):
    try:
        hotel = await HotelsService(db).update_hotel(hotel_id, hotel_data)
        return {"status": "OK", "data": hotel}
    except HotelNotFoundException:
        raise HotelNotFoundHttpException


@router.put("/{hotel_id}", dependencies=[Depends(get_admin_user)])
async def rewrite_hotel(hotel_id: int, hotel_data: HotelAddSchema, db: DBDep):
    try:
        hotel = await HotelsService(db).update_hotel(hotel_id, hotel_data)
        return {"status": "OK", "data": hotel}
    except HotelNotFoundException:
        raise HotelNotFoundHttpException
