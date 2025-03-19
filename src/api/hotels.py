from fastapi import APIRouter, Body, HTTPException, Query
from src.repositories.exceptions import ItemNotFoundException
from src.repositories.hotels import HotelsRepository
from src.models.hotels import HotelsOrm
from src.api.dependencies import PaginationDep
from src.schemas.hotels import HotelPatchSchema, HotelSchema
from src.database import async_session_maker
from sqlalchemy import func, insert, select, delete, update

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(description="Title", default=None),
    location: str | None = Query(description="Location", default=None),
):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            offset=(pagination.page - 1) * pagination.per_page,
            limit=pagination.per_page,
        )


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
        hotels_repo = HotelsRepository(session)
        hotel = await hotels_repo.add(**hotel_data.model_dump())
        await hotels_repo.commit()

        return {"status": "OK", "data": hotel}


# patch, put
@router.patch("/{hotel_id}")
async def update_hotel(hotel_id: int, hotel_data: HotelPatchSchema):
    try:
        async with async_session_maker() as session:
            hotels_repo = HotelsRepository(session)
            hotel = await hotels_repo.update(hotel_id, **hotel_data.model_dump())
            await hotels_repo.commit()
            return {"status": "OK", "data": hotel}
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Item not found")


@router.put("/{hotel_id}")
async def rewrite_hotel(
    hotel_id: int,
    hotel_data: HotelSchema,
):
    try:
        async with async_session_maker() as session:
            hotels_repo = HotelsRepository(session)
            hotel = await hotels_repo.update(hotel_id, **hotel_data.model_dump())
            await hotels_repo.commit()
            return {"status": "OK", "data": hotel}
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Item not found")
