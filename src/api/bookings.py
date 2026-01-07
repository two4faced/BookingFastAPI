from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep, PaginationDep
from src.exceptions import ObjectNotFoundException, AllRoomsBookedException
from src.schemas.bookings import BookingsAdd, BookingsAddRequest

router = APIRouter(prefix='/bookings', tags=['Бронирования'])


@router.get('')
async def get_bookings(db: DBDep, pagination: PaginationDep):
    per_page = pagination.per_page or 5

    return await db.bookings.get_all(limit=per_page, offset=per_page * (pagination.page - 1))


@router.get('/me', summary='Получить свои бронирования')
async def get_my_bookings(
    user_id: UserIdDep,
    db: DBDep,
):
    return await db.bookings.get_all(user_id=user_id)


@router.post('')
async def book_room(user_id: UserIdDep, booking_data: BookingsAddRequest, db: DBDep):
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail='Номер не найден')
    hotel = await db.hotels.get_one(id=room.hotel_id)
    price = room.price * (booking_data.date_to - booking_data.date_from).days

    _booking_data = BookingsAdd(
        user_id=user_id,
        price=price,
        **booking_data.model_dump(),
    )
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    except AllRoomsBookedException as exc:
        raise HTTPException(status_code=409, detail=exc.detail)

    await db.commit()
    return {'status': 'OK', 'data': booking}
