import json
from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient
import pytest
from src.schemas.rooms import RoomsDbSchema
from src.schemas.hotels import HotelAddSchema
from src.database import engine_null_pool, Base
from src.models import * # noqa: F403
from src.config import settings
from src.main import app
from src.utils.db_manager import DBManager
from src.api.dependencies import get_db, get_db_manager_null_pull

TEST_USERNAME = "amdin"
TEST_PASSWORD = "12345678"


@pytest.fixture(autouse=True, scope="session")
async def check_mode() -> None:
    assert settings.MODE == "TEST"


async def get_db_null_pool() -> AsyncGenerator[DBManager, None]:
    async with get_db_manager_null_pull() as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager, None]:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture()
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(autouse=True, scope="session")
async def setup_database(check_mode) -> None:
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(autouse=True, scope="session")
async def create_user(setup_database):
    json_data = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD,
        "password_confirm": TEST_PASSWORD,
    }
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        response = await ac.post("/auth/register", json=json_data)
        data = response.json()
        assert response.status_code == 200
        assert data["username"] == json_data["username"]


@pytest.fixture(autouse=True, scope="session")
async def add_hotels(setup_database):
    async with get_db_manager_null_pull() as db:
        with open("tests/mock_hotels.json", "r") as f:
            data = json.loads(f.read())
            hotels_data = [HotelAddSchema.model_validate(n) for n in data]
        await db.hotels.add_bulk(hotels_data)
        await db.commit()
        hotels_in_db = await db.hotels.get_filtered()
        assert len(hotels_data) == len(hotels_in_db)


@pytest.fixture(autouse=True, scope="session")
async def add_rooms(add_hotels):
    async with get_db_manager_null_pull() as db:
        with open("tests/mock_rooms.json", "r") as f:
            data = json.loads(f.read())
            rooms_data = [RoomsDbSchema.model_validate(n) for n in data]
        await db.rooms.add_bulk(rooms_data)
        await db.commit()
        rooms_in_db = await db.rooms.get_filtered()
        assert len(rooms_in_db) == len(rooms_in_db)
