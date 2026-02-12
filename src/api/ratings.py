from fastapi import APIRouter

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.ratings import RatingRequestAdd
from src.services.ratings import RatingService

router = APIRouter(prefix='/ratings', tags=['Отзывы'])


@router.post('/{hotel_id}')
async def add_rating(data: RatingRequestAdd, hotel_id: int,
                     user_id: UserIdDep, db: DBDep):
    rating = await RatingService(db).add_rating(data, hotel_id, user_id)
    return rating