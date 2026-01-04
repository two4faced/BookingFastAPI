from datetime import date

from fastapi import HTTPException
from sqlalchemy import select

from src.models.bookings import BookingsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import BookingsAdd


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsORM)
            .filter(BookingsORM.date_from == date.today)
        )
        res = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(bookings) for bookings in res.scalars().all()]


    async def add_booking(self, data: BookingsAdd, hotel_id: int):
        query = rooms_ids_for_booking(
            date_from=data.date_from,
            date_to=data.date_to,
            hotel_id=hotel_id
        )
        rooms_ids_to_book_res = await self.session.execute(query)
        rooms_ids_to_book: list[int] = rooms_ids_to_book_res.scalars().all()

        if data.room_id in rooms_ids_to_book:
            new_booking = await self.add(data)
            return new_booking
        else:
            raise HTTPException(404, 'Данную комнату невозможно забронировать')
