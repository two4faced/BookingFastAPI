from pydantic import BaseModel
from sqlalchemy import insert, select

from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.schemas.rooms import Rooms


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Rooms

    async def add_room(self, data: BaseModel, id: int):
        add_stmt = insert(RoomsORM).values(hotel_id=id, **data.model_dump()).returning(self.model)
        result = await self.session.execute(add_stmt)
        model = result.scalars().one()
        inserted_data = self.schema.model_validate(model, from_attributes=True)

        return inserted_data