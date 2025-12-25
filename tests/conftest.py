import pytest
from httpx import AsyncClient, ASGITransport
import json

from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomsAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def add_data(setup_database):
    with open('tests/mock_hotels.json', 'r', encoding='utf-8') as data:
        data_hotels = json.load(data)

    with open('tests/mock_rooms.json', 'r', encoding='utf-8') as data:
        data_rooms = json.load(data)

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        for hotel in data_hotels:
            await db.hotels.add(HotelAdd(title=hotel['title'], location=hotel['location']))
        for room in data_rooms:
            await db.rooms.add(RoomsAdd(
                title=room['title'],
                description=room['description'],
                price=room['price'],
                quantity=room['quantity'],
                hotel_id=room['hotel_id'])
            )
        await db.commit()


@pytest.fixture(scope="session", autouse=True)
async def register_user(add_data):
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        await ac.post(
            '/auth/register',
            json={
                'name': 'pytest',
                'nickname': 'pytest',
                'email': 'coolemail@mail.ru',
                'password': 'pytest1234'
            }
        )
