from src.models.facilities import FacilitiesORM, RoomFacilitiesORM
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facilities, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    schema = Facilities


class RoomFacilitiesRepository(BaseRepository):
    model = RoomFacilitiesORM
    schema = RoomFacility
