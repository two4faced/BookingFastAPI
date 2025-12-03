from sqlalchemy import select

from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsORM
    schema = Hotel

    # async def get_all(
    #         self,
    #         location,
    #         title,
    #         limit,
    #         offset,
    # ) -> list[Hotel]:
    #     query = select(HotelsORM)
    #     if location:
    #         query = query.filter(HotelsORM.location.icontains(location.strip()))
    #     if title:
    #         query = query.filter(HotelsORM.title.icontains(title.strip()))
    #
    #     print(query)
    #
    #     query = (
    #         query
    #         .limit(limit)
    #         .offset(offset)
    #     )
    #     result = await self.session.execute(query)
    #
    #     return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]

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
