from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete

from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None


    def __init__(self, session):
        self.session = session

    async def get_all(self, *filter, **filter_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(elem) for elem in result.scalars().all()]

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        res = result.scalars().one_or_none()
        if res is None:
            return None
        else:
            return self.mapper.map_to_domain_entity(res)

    async def add(self,  data: BaseModel):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_stmt)
        model = result.scalars().one()
        inserted_data = self.mapper.map_to_domain_entity(model)

        return inserted_data

    async def add_batch(self,  data: list[BaseModel]):
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_stmt)


    async def delete(self, **filter_by) -> None:
        del_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(del_stmt)

    async def edit(self, data: BaseModel, is_patch: bool = False, **filter_by) -> None:
        values_to_update = data.model_dump(exclude_unset=is_patch)

        filtered_values = {k: v for k, v in values_to_update.items() if v is not None}

        if not filtered_values:
            return

        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**filtered_values)
        )
        await self.session.execute(update_stmt)