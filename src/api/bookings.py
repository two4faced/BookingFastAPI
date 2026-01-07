from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep, PaginationDep
from src.exceptions import AllRoomsBookedException, AllRoomsBookedHTTPException, RoomNotFoundException, \
    RoomNotFoundHTTPException
from src.schemas.bookings import BookingsAddRequest
from src.services.bookings import BookingsService

router = APIRouter(prefix='/bookings', tags=['Бронирования'])


@router.get('')
async def get_bookings(db: DBDep):
    return await BookingsService(db).get_bookings()


@router.get('/me', summary='Получить свои бронирования')
async def get_my_bookings(
    user_id: UserIdDep,
    db: DBDep,
):
    return await BookingsService(db).get_my_bookings(user_id)


@router.post('')
async def book_room(user_id: UserIdDep, booking_data: BookingsAddRequest, db: DBDep):
    try:
        booking = await BookingsService(db).book_room(user_id, booking_data)
    except AllRoomsBookedException:
        raise AllRoomsBookedHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    await db.commit()
    return {'status': 'OK', 'data': booking}
