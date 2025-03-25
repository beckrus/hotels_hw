from fastapi import APIRouter, Body, HTTPException, Query
from schemas.facilities import FacilitiesAddSchema
from src.repositories.exceptions import ItemNotFoundException
from src.api.dependencies import DBDep, UserIdAdminDep

router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("")
async def get_facilities(
    db: DBDep,
    name: str | None = Query(description="Name", default=None),
):
    filter = {"name":name} if name else {}
    return await db.facilities.get_filtered(**filter)


@router.get("/{facility_id}")
async def get_facility_by_id(facility_id: int, db: DBDep):
    try:
        return await db.facilities.get_one_by_id(id=facility_id)
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Item not found")




@router.post("")
async def create_facility(
    auth_user_id: UserIdAdminDep,
    db: DBDep,
    data: FacilitiesAddSchema = Body(
        openapi_examples={
            "1": {
                "summary": "Wi-Fi",
                "value": {"name": "Wi-fi"},
            },
            "2": {
                "summary": "TV",
                "value": {"name": "TV"},
            },
        }
    ),
):
    facility = await db.facilities.add(data)
    await db.commit()
    return {"status": "OK", "data": facility}


@router.patch("/{facility_id}")
async def update_facility(
    facility_id: int, data: FacilitiesAddSchema, auth_user_id: UserIdAdminDep, db: DBDep
):
    try:
        facility = await db.facilities.edit(facility_id, data, exclude_unset=True)
        await db.commit()
        return {"status": "OK", "data": facility}
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/{facility_id}")
async def delete_facility(facility_id: int, auth_user_id: UserIdAdminDep, db: DBDep):
    try:
        await db.facilities.delete(id=facility_id)
        await db.commit()
        return {"status": "OK"}
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="Item not found")
