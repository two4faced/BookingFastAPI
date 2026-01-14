from datetime import date

from src.schemas.bookings import BookingsAdd, BookingsAddRequest
from src.utils.db_manager import DBManager


async def test_booking_crud(db: DBManager):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingsAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2024, month=8, day=10),
        date_to=date(year=2024, month=8, day=20),
        price=100,
    )

    new_booking = await db.bookings.add(booking_data)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)

    assert booking
    assert booking.id == new_booking.id
    assert booking.room_id == new_booking.room_id
    assert booking.user_id == new_booking.user_id

    updated_date = date(year=2024, month=8, day=18)
    await db.bookings.edit(
        data=BookingsAddRequest(
            room_id=booking.room_id,
            date_from=date(year=2024, month=8, day=10),
            date_to=updated_date,
        ),
        id=new_booking.id,
    )

    edited_booking = await db.bookings.get_one_or_none(id=new_booking.id)

    assert edited_booking
    assert edited_booking.id == new_booking.id
    assert edited_booking.date_to == updated_date

    await db.bookings.delete(id=booking.id)
    assert await db.bookings.get_one_or_none(id=booking.id) is None
