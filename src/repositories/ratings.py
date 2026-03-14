from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.models import RatingsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RatingsDataMapper
from src.schemas.ratings import Rating


class RatingsRepository(BaseRepository):
    model = RatingsORM
    mapper = RatingsDataMapper

    async def get_all(self, *filter, **filter_by) -> list[Rating]:
        query = (
            select(self.model)
            .options(joinedload(self.model.user))
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(elem) for elem in result.scalars().unique().all()]
