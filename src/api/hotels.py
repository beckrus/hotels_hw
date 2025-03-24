from fastapi import APIRouter, Body, HTTPException, Query
from src.repositories.exceptions import ItemNotFoundException
from src.api.dependencies import DBDep, PaginationDep, UserIdAdminDep
from src.schemas.hotels import HotelAddSchema, HotelPatchSchema

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(description="Title", default=None),
    location: str | None = Query(description="Location", default=None),
):
    return await db.hotels.get_all(
        location=location,
        title=title,
        offset=(pagination.page - 1) * pagination.per_page,
        limit=pagination.per_page,
    )


@router.get("/{id}")
async def get_hotel_by_id(id: int, db: DBDep):
    try:
        return await db.hotels.get_one_by_id(id=id)
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, auth_user_id: UserIdAdminDep, db: DBDep):
    try:
        await db.hotels.delete(id=hotel_id)
        await db.commit()
        return {"status": "OK"}
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Item not found")


@router.post("")
async def create_hotel(
    auth_user_id: UserIdAdminDep,
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
@router.patch("/{hotel_id}")
async def update_hotel(
    hotel_id: int, hotel_data: HotelPatchSchema, auth_user_id: UserIdAdminDep, db: DBDep
):
    try:
        hotel = await db.hotels.edit(hotel_id, hotel_data, exclude_unset=True)
        await db.commit()
        return {"status": "OK", "data": hotel}
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Item not found")


@router.put("/{hotel_id}")
async def rewrite_hotel(
    auth_user_id: UserIdAdminDep, hotel_id: int, hotel_data: HotelAddSchema, db: DBDep
):
    try:
        hotel = await db.hotels.edit(hotel_id, hotel_data)
        await db.commit()
        return {"status": "OK", "data": hotel}
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Item not found")
