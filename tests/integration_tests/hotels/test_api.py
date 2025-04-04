from datetime import date, timedelta


async def test_get_hotels(ac):
    date_from = date.today().strftime("%Y-%m-%d")
    date_to = (date.today() + timedelta(days=10)).strftime("%Y-%m-%d")
    res = await ac.get("/hotels", params={"date_from": date_from, "date_to": date_to})
    data = res.json()
    assert res.status_code == 200
    assert len(data) > 0
    res_limit_1 = await ac.get(
        "/hotels",
        params={
            "date_from": date_from,
            "date_to": date_to,
            "page": 1,
            "per_page": 1,
        },
    )
    data_limit_1 = res_limit_1.json()
    assert res_limit_1.status_code == 200
    assert len(data_limit_1) == 1
