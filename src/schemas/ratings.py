from pydantic import BaseModel, ConfigDict, conint, Field


class RatingRequestAdd(BaseModel):
    rating: conint(ge=1, le=5)  # type: ignore
    rating_text: str

    model_config = ConfigDict(from_attributes=True)


class RatingAdd(RatingRequestAdd):
    user_id: int
    hotel_id: int

    model_config = ConfigDict(from_attributes=True)


class Rating(RatingAdd):
    id: int
    user_name: str

    model_config = ConfigDict(from_attributes=True)


class RatingPatch(BaseModel):
    rating: conint(ge=1, le=5) | None = Field(None)  # type: ignore
    rating_text: str | None = Field(None, max_length=1000)

    model_config = ConfigDict(from_attributes=True)
