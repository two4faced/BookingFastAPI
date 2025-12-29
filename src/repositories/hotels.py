from sqlalchemy import select

from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import HotelDataMapper
from src.repositories.utils import rooms_ids_for_booking


class HotelsRepository(BaseRepository):
    model = HotelsORM
    mapper = HotelDataMapper


    async def get_filtered_by_time(
            self,
            date_from,
            date_to,
            location,
            title,
            offset,
            limit
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to)

        hotels_ids = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
        )

        if location:
            hotels_ids = hotels_ids.filter(HotelsORM.location.icontains(location.strip()))
        if title:
            hotels_ids = hotels_ids.filter(HotelsORM.title.icontains(title.strip()))

        hotels_ids = (
            hotels_ids
            .limit(limit)
            .offset(offset)
        )

        return await self.get_all(HotelsORM.id.in_(hotels_ids))
