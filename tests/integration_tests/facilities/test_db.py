from src.schemas.facilities import FacilitiesAddSchema
from src.utils.db_manager import DBManager


async def test_facilities_crud(db: DBManager):
    f_data = FacilitiesAddSchema(name="Wi-Fi")
    f_added = await db.facilities.add(f_data)
    assert f_added

    f_get = await db.facilities.get_one_or_none(id=f_added.id)
    assert f_get

    f_data.name = "TV"
    f_updated = await db.facilities.edit(f_get.id, f_data)
    assert f_updated.name == f_data.name

    await db.facilities.delete(f_updated.id)
    await db.commit()

    booking_get_after_del = await db.facilities.get_one_or_none(id=f_updated.id)
    assert not booking_get_after_del
