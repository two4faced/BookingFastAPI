from src.models import RatingsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RatingsDataMapper


class RatingsRepository(BaseRepository):
    model = RatingsORM
    mapper = RatingsDataMapper
