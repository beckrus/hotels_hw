from fastapi import APIRouter, Body, HTTPException, Query
from src.models.hotels import HotelsOrm
from src.api.dependencies import PaginationDep
from src.schemas.hotels import HotelPatchSchema, HotelSchema
from src.database import async_session_maker
from sqlalchemy import insert, select, delete, update

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(description="Title", default=None),
    location: str | None = Query(description="Location", default=None),
):
    offset = (pagination.page - 1) * pagination.per_page
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if location:
            query = query.where(HotelsOrm.location.ilike(f"%{location}%"))
        if title:
            query = query.where(HotelsOrm.title.ilike(f"%{title}%"))
        query = query.limit(pagination.per_page).offset(offset)
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels


@router.delete("/{hotel_id}")
async def delete_hotel(
    hotel_id: int,
):
    async with async_session_maker() as session:
        query = select(HotelsOrm).filter_by(id=hotel_id)
        res = await session.execute(query)
        hotel = res.scalar_one_or_none()
        if hotel:
            await session.delete(hotel)
            await session.commit()
            return {"status": "OK"}
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("")
async def create_hotel(
    hotel_data: HotelSchema = Body(
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
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()

    return hotel_data


# patch, put
@router.patch("/{hotel_id}")
async def update_hotel(hotel_id: int, hotel_data: HotelPatchSchema):
    async with async_session_maker() as session:
        query = select(HotelsOrm).filter_by(id=hotel_id)
        result = await session.execute(query)
        hotel = result.scalar_one_or_none()
        if hotel:
            stmt = (
                update(HotelsOrm)
                .filter_by(id=hotel_id)
                .values(**hotel_data.model_dump())
            )
            await session.execute(stmt)
            await session.commit()
            return {"status": "OK"}
    raise HTTPException(status_code=404, detail="Item not found")


@router.put("/{hotel_id}")
async def rewrite_hotel(
    hotel_id: int,
    hotel_data: HotelSchema,
):
    async with async_session_maker() as session:
        query = select(HotelsOrm).filter_by(id=hotel_id)
        result = await session.execute(query)
        hotel = result.scalar_one_or_none()
        if hotel:
            stmt = (
                update(HotelsOrm)
                .filter_by(id=hotel_id)
                .values(**hotel_data.model_dump())
            )
            await session.execute(stmt)
            await session.commit()
            return {"status": "OK"}
    raise HTTPException(status_code=404, detail="Item not found")
