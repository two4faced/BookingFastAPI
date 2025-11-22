from pydantic import BaseModel, Field, ConfigDict


class RoomsAdd(BaseModel):
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)

class Rooms(RoomsAdd):
    id: int
    hotel_id: int

class RoomsPatch(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)

    model_config = ConfigDict(from_attributes=True)