from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, EmailStr


class UserSchema(BaseModel):
    email: EmailStr
    password: str = Field(max_length=120)

    class Config:
        extra = 'forbid'


class UserRegisterSchema(UserSchema):
    name: Optional[str] = Field(min_length=2, max_length=100)
    surname: Optional[str] = Field(min_length=2, max_length=100)
    bio: Optional[str] = Field(max_length=300)
    age: Optional[int] = Field(ge=0, le=130)
    gender: Optional[Literal['male', 'female']] = None

    class Config:
        extra = 'forbid'


class BookAddSchema(BaseModel):
    title: str
    author: str


class BookSchema(BookAddSchema):
    id: int
