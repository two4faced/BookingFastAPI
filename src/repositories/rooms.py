from datetime import date

from sqlalchemy import func, select

from src.database import engine
from src.models.bookings import BookingsORM
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
        rooms_count = (
            select(BookingsORM.room_id, func.count('*').label('rooms_booked'))
            .select_from(BookingsORM)
            .filter(
                BookingsORM.date_from <= date_to,
                BookingsORM.date_to >= date_from
            )
            .group_by(BookingsORM.room_id)
            .cte(name='rooms_count')
        )

        rooms_left_table = (
            select(
                RoomsORM.id.label('room_id'),
                (RoomsORM.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label('rooms_left')
            )
            .select_from(RoomsORM)
            .outerjoin(rooms_count, RoomsORM.id == rooms_count.c.room_id)
            .cte(name='rooms_left')
        )

        query = (
            select(rooms_left_table)
            .select_from(rooms_left_table)
            .filter(rooms_left_table.c.rooms_left > 0)
        )

        print(query.compile(bind=engine, compile_kwargs={'literal_binds': True}))
