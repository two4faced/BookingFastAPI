from pydantic import BaseModel, ConfigDict, conint


class RatingRequestAdd(BaseModel):
    rating: int | conint(ge=1, le=5)
    rating_text: str

    model_config = ConfigDict(from_attributes=True)


class RatingAdd(RatingRequestAdd):
    user_id: int
    hotel_id: int

    model_config = ConfigDict(from_attributes=True)


class Rating(RatingAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)