from src.models.users import UsersORM
from src.repositories.base import BaseRepository
from src.schemas.users import User


class RoomsRepository(BaseRepository):
    model = UsersORM
    schema = User