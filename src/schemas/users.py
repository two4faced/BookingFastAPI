from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserLogIn(BaseModel):
    email: EmailStr | None = Field(None)
    password: str = Field(min_length=10)


class UserRequestAdd(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr
    password: str = Field(min_length=10)


class UserAdd(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr
    hashed_password: str


class User(BaseModel):
    id: int
    name: str = Field(min_length=3)
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserWithHashedPassword(User):
    hashed_password: str
