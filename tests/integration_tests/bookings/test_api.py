from datetime import date, timedelta
from utils.db_manager import DBManager


async def test_get_bookings(authenticated_ac):
    res = await authenticated_ac.get("/bookings/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

async def test_get_bookings(ac):
    res_wo_auth = await ac.get("/bookings/")
    assert res_wo_auth.status_code == 401


async def test_post_bookings_wo_auth(ac):
    res_add_wo_auth = await ac.post("/bookings/")
    assert res_add_wo_auth.status_code == 401


async def test_post_bookings_w_auth(db: DBManager, authenticated_ac):
    room_id = (await db.rooms.get_all())[0].id
    date_from = date.today().strftime("%Y-%m-%d")
    date_to = (date.today() + timedelta(days=10)).strftime("%Y-%m-%d")
    res_add = await authenticated_ac.post("/bookings/",
                                json={
                                    "room_id": room_id,
                                    "date_from": date_from,
                                    "date_to": date_to,
                                }
                                )
    res_data = res_add.json()
    assert res_add.status_code == 200
    assert res_data['status'] == "OK"
    assert isinstance(res_data, dict)
    assert res_data['data']['room_id'] == room_id
    assert res_data['data']['date_from'] == date_from
    assert res_data['data']['date_to'] == date_to