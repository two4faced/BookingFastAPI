from pydantic import EmailStr
from sqlalchemy import select

from src.models.users import UsersORM
from src.repositories.base import BaseRepository
from src.schemas.users import User, UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersORM
    schema = User

    async def get_user_with_hashed_pass(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        res = result.scalars().one()
        return UserWithHashedPassword.model_validate(res, from_attributes=True)
