from sqlalchemy import delete, and_
from sqlalchemy.dialects.postgresql import insert as pg_insert

from src.models.facilities import FacilitiesORM, RoomFacilitiesORM
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facilities, RoomFacility
from src.schemas.rooms import RoomsPatch


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    schema = Facilities


class RoomFacilitiesRepository(BaseRepository):
    model = RoomFacilitiesORM
    schema = RoomFacility

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