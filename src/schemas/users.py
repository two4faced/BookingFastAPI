from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserLogIn(BaseModel):
    email: EmailStr | None = Field(None)
    password: str


class UserRequestAdd(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserAdd(BaseModel):
    name: str
    email: EmailStr
    hashed_password: str


class User(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserWithHashedPassword(User):
    hashed_password: str
