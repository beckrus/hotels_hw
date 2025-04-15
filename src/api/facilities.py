from fastapi import APIRouter, Body, Depends, Query
from fastapi_cache.decorator import cache

from src.schemas.facilities import FacilitiesAddSchema
from src.services.facilities import FacilitiesService
from src.exceptions import (
    FacilityDuplicateException,
    FacilityDuplicateHTTPException,
    FacilityNotFoundException,
    FacilityNotFoundHttpException,
)
from src.api.dependencies import DBDep, get_current_user


router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("")
@cache(expire=1)
async def get_facilities(
    db: DBDep,
    name: str | None = Query(description="Name", default=None),
):
    return await FacilitiesService(db).get_facilities(name)


@router.get("/{facility_id}")
async def get_facility_by_id(facility_id: int, db: DBDep):
    try:
        return await FacilitiesService(db).get_facility_by_id(facility_id)
    except FacilityNotFoundException:
        raise FacilityNotFoundHttpException


@router.post("", dependencies=[Depends(get_current_user)])
async def create_facility(
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
    try:
        facility = await db.facilities.add(data)
        await db.commit()
        return {"status": "OK", "data": facility}
    except FacilityDuplicateException:
        raise FacilityDuplicateHTTPException


@router.patch("/{facility_id}", dependencies=[Depends(get_current_user)])
async def update_facility(facility_id: int, data: FacilitiesAddSchema, db: DBDep):
    try:
        facility = await FacilitiesService(db).update_facility(facility_id, data)
        return {"status": "OK", "data": facility}
    except FacilityNotFoundException:
        raise FacilityNotFoundHttpException


@router.delete("/{facility_id}", dependencies=[Depends(get_current_user)])
async def delete_facility(facility_id: int, db: DBDep):
    try:
        await FacilitiesService(db).delete(facility_id)
        return {"status": "OK"}
    except FacilityNotFoundException:
        raise FacilityNotFoundHttpException
