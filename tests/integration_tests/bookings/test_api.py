import pytest
from datetime import date, timedelta
from tests.conftest import get_db_null_pool


async def test_get_bookings(authenticated_ac):
    res = await authenticated_ac.get("/bookings/")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert data["status"] == "OK"
    assert "data" in data


async def test_get_bookings_wo_auth(ac):
    res_wo_auth = await ac.get("/bookings/")
    assert res_wo_auth.status_code == 401


async def test_post_bookings_wo_auth(ac):
    res_add_wo_auth = await ac.post("/bookings/")
    assert res_add_wo_auth.status_code == 401


date_from = date.today().strftime("%Y-%m-%d")
date_to = (date.today() + timedelta(days=10)).strftime("%Y-%m-%d")


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, date_from, date_to, 200),
        (1, date_from, date_to, 200),
        (1, date_from, date_to, 200),
        (1, date_from, date_to, 200),
        (1, date_from, date_to, 200),
        (1, date_from, date_to, 409),
        (1, date_from, date_to, 409),
    ],
)
async def test_post_bookings_w_auth(
    room_id: int, date_from: str, date_to: str, status_code: int, authenticated_ac
):
    res_add = await authenticated_ac.post(
        "/bookings/",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    res_data = res_add.json()
    assert res_add.status_code == status_code
    if status_code == 200:
        assert res_data["status"] == "OK"
        assert isinstance(res_data, dict)
        assert res_data["data"]["room_id"] == room_id
        assert res_data["data"]["date_from"] == date_from
        assert res_data["data"]["date_to"] == date_to


@pytest.fixture(scope="module")
async def del_all_bookings():
    async for _db in get_db_null_pool():
        all_bookings = await _db.bookings.get_all()
        await _db.bookings.delete_bulk([n.id for n in all_bookings])
        await _db.commit()
        assert len(await _db.bookings.get_all()) == 0


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code, count",
    [
        (1, date_from, date_to, 200, 1),
        (1, date_from, date_to, 200, 2),
        (1, date_from, date_to, 200, 3),
    ],
)
async def test_add_and_get_my_bookings(
    room_id: int,
    date_from: str,
    date_to: str,
    status_code: int,
    count: int,
    del_all_bookings,
    authenticated_ac,
):
    res_add = await authenticated_ac.post(
        "/bookings/",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert res_add.status_code == status_code
    my_bookings = await authenticated_ac.get("/bookings/me")
    assert my_bookings.status_code == status_code
    data = my_bookings.json()
    assert "data" in data
    assert len(data["data"]) == count


async def test_add_and_delete_bookings(
    authenticated_ac,
):
    my_bookings = await authenticated_ac.get("/bookings/me")
    assert my_bookings.status_code == 200
    data = my_bookings.json()
    assert "data" in data
    bookings_len = len(data["data"])
    res_add = await authenticated_ac.post(
        "/bookings/",
        json={
            "room_id": 1,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert res_add.status_code == 200
    data = res_add.json()
    assert data["data"]["room_id"] == 1

    resp_del = await authenticated_ac.delete(f"/bookings/{data['data']['id']}")
    assert resp_del.status_code == 200
    my_bookings_after_del = await authenticated_ac.get("/bookings/me")
    data_after_del = my_bookings_after_del.json()
    assert "data" in data_after_del
    assert len(data_after_del["data"]) == bookings_len
    resp_del_2 = await authenticated_ac.delete(f"/bookings/{data['data']['id']}")
    assert resp_del_2.status_code == 404
