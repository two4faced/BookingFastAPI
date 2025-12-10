from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from src.repositories.utils import rooms_ids_for_booking
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.schemas.rooms import Rooms, RoomsWithRels


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Rooms

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
        return [RoomsWithRels.model_validate(model) for model in result.scalars().all()]
