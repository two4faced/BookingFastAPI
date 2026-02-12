from src.api.dependencies import UserIdDep
from src.schemas.ratings import RatingAdd, RatingRequestAdd
from src.services.base import BaseService


class RatingService(BaseService):
    async def add_rating(self, rating_data: RatingRequestAdd, hotel_id: int,
                        user_id: UserIdDep):
        _rating_data = RatingAdd(hotel_id=hotel_id, user_id=user_id, **rating_data.model_dump())
        result = await self.db.ratings.add(_rating_data)
        await self.db.commit()

        return result
