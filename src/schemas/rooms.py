from pydantic import BaseModel, Field, ConfigDict


class RoomsAddRequest(BaseModel):
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int
    facilities_ids: list[int] | None = Field(None)

    model_config = ConfigDict(from_attributes=True)


class RoomsAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)

class Rooms(RoomsAdd):
    id: int

class RoomsPatch(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)

    model_config = ConfigDict(from_attributes=True)

class RoomsPatchRequest(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
    facilities_ids: list[int] | None = Field(None)

    model_config = ConfigDict(from_attributes=True)