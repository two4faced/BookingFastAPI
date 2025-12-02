from sqlalchemy import select

from src.models.bookings import BookingsORM
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.schemas.bookings import Bookings
from src.schemas.rooms import Rooms


class BookingsRepository(BaseRepository):
    model = BookingsORM
    schema = Bookings

    async def get_all_bookings(
            self,
            limit,
            offset,
    ) -> list[Rooms]:
        query = select(RoomsORM)
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)

        return [Rooms.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]