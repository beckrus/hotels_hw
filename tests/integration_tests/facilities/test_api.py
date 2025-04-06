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


async def test_post_facilities_wo_auth(ac):
    res_add_wo_auth = await ac.post("/facilities",
                                params={
                                    "name":"Wi-fi"
                                    }
                                )
    assert res_add_wo_auth.status_code == 401


async def test_post_facilities_w_auth(authenticated_ac):
    f_name = "Wi-fi"
    res_add = await authenticated_ac.post("/facilities",
                                json={
                                    "name":f_name
                                    }
                                )
    assert res_add.status_code == 200
    assert res_add.json()['data']['name'] == f_name