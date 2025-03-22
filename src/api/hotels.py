from fastapi import APIRouter, Body, HTTPException, Query
from src.repositories.exceptions import ItemNotFoundException
from src.repositories.hotels import HotelsRepository
from src.api.dependencies import PaginationDep, UserIdAdminDep
from src.schemas.hotels import HotelAddSchema, HotelPatchSchema, HotelSchema
from src.database import async_session_maker

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


@router.get("/{id}")
async def get_hotel_by_id(id: int):
    async with async_session_maker() as session:
        try:
            return await HotelsRepository(session).get_one_by_id(id=id)
        except ItemNotFoundException:
            raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/{hotel_id}")
async def delete_hotel(
    hotel_id: int,
    auth_user_id: UserIdAdminDep
):
    try:
        async with async_session_maker() as session:
            hotels_repo = HotelsRepository(session)
            await hotels_repo.delete(id=hotel_id)
            await hotels_repo.commit()
            return {"status": "OK"}
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Item not found")


@router.post("")
async def create_hotel(
    auth_user_id: UserIdAdminDep,
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
    async with async_session_maker() as session:
        hotels_repo = HotelsRepository(session)
        hotel = await hotels_repo.add(hotel_data)
        await hotels_repo.commit()

        return {"status": "OK", "data": hotel}


# patch, put
@router.patch("/{hotel_id}")
async def update_hotel(hotel_id: int, hotel_data: HotelPatchSchema,auth_user_id: UserIdAdminDep):
    try:
        async with async_session_maker() as session:
            hotels_repo = HotelsRepository(session)
            hotel = await hotels_repo.edit(hotel_id, hotel_data, exclude_unset=True)
            await hotels_repo.commit()
            return {"status": "OK", "data": hotel}
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Item not found")


@router.put("/{hotel_id}")
async def rewrite_hotel(
    auth_user_id: UserIdAdminDep,
    hotel_id: int,
    hotel_data: HotelAddSchema,
):
    try:
        async with async_session_maker() as session:
            hotels_repo = HotelsRepository(session)
            hotel = await hotels_repo.edit(hotel_id, hotel_data)
            await hotels_repo.commit()
            return {"status": "OK", "data": hotel}
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Item not found")
