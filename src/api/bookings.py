from fastapi import APIRouter, Request

from src.api.dependencies import DBDep, get_current_user_id, get_token
from src.schemas.bookings import BookingsAdd, BookingsAddRequest

router = APIRouter(prefix='/bookings', tags=['Бронирования'])


@router.post('')
async def book_room(request: Request, booking_data: BookingsAddRequest, db: DBDep):
    user_id = get_current_user_id(get_token(request))
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    price = room.model_dump().get('price') * (booking_data.date_to - booking_data.date_from).days
    _booking = BookingsAdd(user_id=user_id, price=price, **booking_data.model_dump())
    res = await db.bookings.add(_booking)
    await db.commit()

    return {'status': 'OK', 'data': res}
