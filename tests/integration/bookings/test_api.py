import pytest
from sqlalchemy import delete

from src.database import engine_null_pool, async_session_maker_null_pool
from src.models import BookingsORM
from src.utils.db_manager import DBManager


@pytest.mark.parametrize('room_id, date_from, date_to, status_code', [
    (1, "2024-08-01", "2024-08-10", 200),
    (1, "2024-08-02", "2024-08-11", 200),
    (1, "2024-08-03", "2024-08-12", 200),
    (1, "2024-08-04", "2024-08-13", 200),
    (1, "2024-08-05", "2024-08-14", 200),
    (1, "2024-08-06", "2024-08-15", 404),
    (1, "2024-08-17", "2024-08-25", 200),
                         ])
async def test_add_booking(
        room_id: int,
        date_from: str,
        date_to: str,
        status_code: int,
        db,
        authenticated_ac
):
    response = await authenticated_ac.post(
        '/bookings',
        json={
            'room_id': room_id,
            'date_from': date_from,
            'date_to': date_to,
        }
    )
    result = response.json()

    assert response.status_code == status_code
    if status_code == 200:
        assert 'data' in result
        assert isinstance(result, dict)


@pytest.fixture(scope='module')
async def delete_all_bookings():
    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.bookings.delete()
        await db_.commit()

    assert len(await db_.bookings.get_all()) == 0


@pytest.mark.parametrize('room_id, date_from, date_to, rooms_booked_count', [
    (1, "2024-08-01", "2024-08-10", 1),
    (1, "2024-08-02", "2024-08-11", 2),
    (1, "2024-08-03", "2024-08-12", 3)
])
async def test_add_and_get_bookings(
        room_id: int,
        date_from: str,
        date_to: str,
        rooms_booked_count: int,
        delete_all_bookings,
        authenticated_ac
):
    response_post = await authenticated_ac.post(
        '/bookings',
        json={
            'room_id': room_id,
            'date_from': date_from,
            'date_to': date_to,
        }
    )
    assert response_post.status_code == 200

    response_get_me = await authenticated_ac.get('/bookings/me')

    assert response_post.status_code == 200
    assert len(response_get_me.json()) == rooms_booked_count
