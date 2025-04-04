import json
from typing import Any, AsyncGenerator
from httpx import ASGITransport, AsyncClient
import pytest
from api.dependencies import get_db_manager_null_pull
from src.schemas.rooms import RoomsDbSchema
from src.schemas.hotels import HotelAddSchema
from src.database import engine_null_pool, Base
from src.models import *
from src.config import settings
from src.main import app
from src.utils.db_manager import DBManager


@pytest.fixture(autouse=True, scope="session")
async def check_mode() -> None:
    assert settings.MODE == "TEST"

@pytest.fixture()
async def db() -> AsyncGenerator[DBManager, None]:
    async with get_db_manager_null_pull() as db:
        yield db

@pytest.fixture(scope="session")
async def db_s() -> AsyncGenerator[DBManager, None]:
    async with get_db_manager_null_pull() as db:
        yield db

@pytest.fixture()
async def ac() -> AsyncGenerator[DBManager, None]:
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="session")
async def ac_s() -> AsyncGenerator[DBManager, None]:
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(autouse=True, scope="session")
async def setup_database(check_mode) -> None:
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(autouse=True, scope="session")
async def create_user(setup_database, ac_s: AsyncClient):
    json_data = {
        "username":"admin",
        "password":"12345678",
        "password_confirm":"12345678"
    }
    response = await ac_s.post("/auth/register", json=json_data)
    data = response.json()
    assert response.status_code == 200
    assert data['username'] == json_data['username']

@pytest.fixture(autouse=True, scope="session")
async def add_hotels(setup_database, db_s: DBManager):
    with open('tests/mock_hotels.json', 'r') as f:
        data = json.loads(f.read())
        hotels_data = [HotelAddSchema.model_validate(n) for n in data]
    await db_s.hotels.add_bulk(hotels_data)
    await db_s.commit()
    hotels_in_db = await db_s.hotels.get_filtered()
    assert len(hotels_data) == len(hotels_in_db)

@pytest.fixture(autouse=True, scope="session")
async def add_rooms(add_hotels, db_s: DBManager):
    with open('tests/mock_rooms.json', 'r') as f:
        data = json.loads(f.read())
        rooms_data = [RoomsDbSchema.model_validate(n) for n in data]
    await db_s.rooms.add_bulk(rooms_data)
    await db_s.commit()
    rooms_in_db = await db_s.rooms.get_filtered()
    assert len(rooms_in_db) == len(rooms_in_db)


