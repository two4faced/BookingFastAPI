from sqlalchemy import select

from src.models.hotels import HotelsORM
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsORM

    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
    ):
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

        return result.scalars().all()
