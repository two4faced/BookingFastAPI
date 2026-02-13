from src.api.dependencies import UserIdDep
from src.exceptions import ObjectNotFoundException, HotelNotFoundException
from src.schemas.ratings import RatingAdd, RatingRequestAdd
from src.services.base import BaseService


class RatingService(BaseService):
    async def get_ratings(self, hotel_id: int):
        return await self.db.ratings.get_all(hotel_id=hotel_id)


    async def add_rating(self, rating_data: RatingRequestAdd, hotel_id: int, user_id: UserIdDep):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as exc:
            raise HotelNotFoundException from exc

        _rating_data = RatingAdd(hotel_id=hotel_id, user_id=user_id, **rating_data.model_dump())
        result = await self.db.ratings.add(_rating_data)
        await self.db.commit()

        return result
