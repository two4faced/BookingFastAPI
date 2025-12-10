from datetime import date


from src.repositories.utils import rooms_ids_for_booking
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.schemas.rooms import Rooms


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
        return await self.get_all(RoomsORM.id.in_(rooms_ids_to_get))
