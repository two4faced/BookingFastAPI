from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.repositories.mappers.mappers import RoomsDataMapper, RoomsWithRelsDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository


class RoomsRepository(BaseRepository):
    model = RoomsORM
    mapper = RoomsDataMapper

    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id=hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
        )

        result = await self.session.execute(query)
        return [RoomsWithRelsDataMapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_one_or_none(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        res = result.scalars().one_or_none()
        if res is None:
            return None
        else:
            return RoomsWithRelsDataMapper.map_to_domain_entity(res)
