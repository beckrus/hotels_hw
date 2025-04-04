async def test_get_facilities(ac):
    res = await ac.get("/facilities")
    data = res.json()
    assert res.status_code == 200
    assert isinstance(data, list)
    res_add_wo_auth = await ac.post("/facilities",
                                params={
                                    "name":"Wi-fi"
                                    }
                                )
    assert res_add_wo_auth.status_code == 401
