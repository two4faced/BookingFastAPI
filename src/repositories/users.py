from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    model = RoomsORM