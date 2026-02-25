# ruff: noqa: E402
from typing import AsyncGenerator, Any

import pytest
from httpx import AsyncClient, ASGITransport
import json
from unittest import mock

mock.patch('fastapi_cache.decorator.cache', lambda *args, **kwargs: lambda f: f).start()

from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *  # noqa
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomsAdd
from src.utils.db_manager import DBManager


@pytest.fixture()
async def db() -> AsyncGenerator[DBManager, Any]:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='session', autouse=True)
def check_test_mode():
    assert settings.MODE == 'TEST'


@pytest.fixture(scope='session', autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope='session', autouse=True)
async def add_data(setup_database):
    with open('tests/mock_hotels.json', 'r', encoding='utf-8') as data:
        data_hotels = json.load(data)

    with open('tests/mock_rooms.json', 'r', encoding='utf-8') as data:
        data_rooms = json.load(data)

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        for hotel in data_hotels:
            await db_.hotels.add(HotelAdd.model_validate(hotel))
        for room in data_rooms:
            await db_.rooms.add(RoomsAdd.model_validate(room))
        await db_.commit()


@pytest.fixture(scope='session', autouse=True)
async def register_user(add_data, ac):
    await ac.post(
        '/auth/register',
        json={
            'name': 'pytest',
            'email': 'coolemail@mail.ru',
            'password': 'pytest1234',
        },
    )


@pytest.fixture(scope='session')
async def authenticated_ac(register_user, ac):
    response = await ac.post(
        '/auth/login', json={'email': 'coolemail@mail.ru', 'password': 'pytest1234'}
    )

    assert response.status_code == 200
    assert ac.cookies['access_token']

    yield ac
