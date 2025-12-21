from datetime import date

from sqlalchemy import select

from src.models.bookings import BookingsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.schemas.bookings import Bookings


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper

    async def get_all_bookings(
            self,
            limit,
            offset,
    ) -> list[Bookings]:
        query = select(BookingsORM)
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(bookings) for bookings in result.scalars().all()]

    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsORM)
            .filter(BookingsORM.date_from == date.today)
        )
        res = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(bookings) for bookings in res.scalars().all()]