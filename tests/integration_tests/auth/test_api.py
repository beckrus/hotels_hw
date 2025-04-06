import pytest
from tests.conftest import TEST_USERNAME, TEST_PASSWORD

@pytest.mark.parametrize(
    "username, email, password, password_confirm, status_code",
    [
        ('admin','','password','password',422),
        ('admin','admin@example.com','','password',422),
        ('admin','admin@example.com','','',422),
        ('admin','admin@example.com','password','',422),
        ('admin','admin@example.com','password','password',400),
        ('user','admin@example.com','password','',422),
        ('user','user@example.com','password','password',200),
        ('user2','user2@example.com','password','password',200),
        ('user3','user2@example','password','password',422),
        ('user4','user2@example.com','111','111',422),
    ],
)
async def test_post_register(
    username:str,
    email:str,
    password:str,
    password_confirm:str,
    status_code:int,
    ac,
):
    res_add = await ac.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
            "password_confirm": password_confirm,
        },
    )
    assert res_add.status_code == status_code


@pytest.mark.parametrize(
    "username, password, status_code",
    [
        (TEST_USERNAME,TEST_PASSWORD,200),
        (TEST_USERNAME,'',401),
        ('','password',401),
        ('user','password',200),
        ('user2','password',200),
    ],
)
async def test_post_login_me_logout(
    username:str,
    password:str,
    status_code:int,
    ac,
):
    res_add = await ac.post(
        "/auth/login",
        data={
            "grant_type": "string",
            "username": username,
            "password": password,
        },
    )
    assert res_add.status_code == status_code
    if status_code == 200:
        assert ac.cookies.get("access_token")

        res_me = await ac.get("/auth/me")
        assert res_me.status_code == status_code
        data = res_me.json()
        assert isinstance(data, dict)
        assert data["username"] == username
        
        res_logout = await ac.post("/auth/logout")
        assert res_logout.status_code == 200
        assert ac.cookies.get("access_token") is None
