from sqlalchemy import select

from src.models.hotels import HotelsORM
from src.repositories.base import BaseRepository
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsORM
    schema = Hotel

    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
    ) -> list[Hotel]:
        query = select(HotelsORM)
        if location:
            query = query.filter(HotelsORM.location.icontains(location.strip()))
        if title:
            query = query.filter(HotelsORM.title.icontains(title.strip()))

        print(query)

        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)

        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]
