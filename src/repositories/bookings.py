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

        return [Bookings.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]