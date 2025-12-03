from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete


class BaseRepository:
    model = None
    schema: BaseModel = None
    def __init__(self, session):
        self.session = session

    async def get_all(self, *filter, **filter_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(elem, from_attributes=True) for elem in result.scalars().all()]

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        res = result.scalars().one_or_none()
        if res is None:
            return None
        else:
            return self.schema.model_validate(res, from_attributes=True)

    async def add(self,  data: BaseModel):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_stmt)
        model = result.scalars().one()
        inserted_data = self.schema.model_validate(model, from_attributes=True)

        return inserted_data

    async def delete(self, **filter_by) -> None:
        del_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(del_stmt)

    async def edit(self,  data: BaseModel, is_patch: bool = False, **filter_by) -> None:
        edit_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=is_patch)))
        await self.session.execute(edit_stmt)