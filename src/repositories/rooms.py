from datetime import date

from sqlalchemy import delete, and_
from sqlalchemy.dialects.postgresql import insert as pg_insert

from src.models.facilities import RoomFacilitiesORM
from src.repositories.utils import rooms_ids_for_booking
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.schemas.rooms import Rooms, RoomsPatch


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

    async def change_room_facilities(
            self,
            room_id: int,
            data: RoomsPatch,
    ):

        data_to_insert = [
            {'room_id': room_id, 'facility_id': facility_id}
            for facility_id in data.facilities_ids
        ]

        insert_stmt = pg_insert(RoomFacilitiesORM).values(data_to_insert)
        insert_stmt = insert_stmt.on_conflict_do_nothing(index_elements=['room_id', 'facility_id'])

        await self.session.execute(insert_stmt)

        condition = and_(
        RoomFacilitiesORM.room_id == room_id,
        RoomFacilitiesORM.facility_id.not_in(data.facilities_ids)
    )

        delete_stmt = delete(RoomFacilitiesORM).where(condition)

        await self.session.execute(delete_stmt)
