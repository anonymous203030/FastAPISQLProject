from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, EmailStr


class UserSchema(BaseModel):
    email: EmailStr
    password: str = Field(max_length=120)
    model_config = ConfigDict(extra='forbid')


class UserDetailsSchema(UserSchema):
    name: str = Field(min_length=2, max_length=100)
    surname: str = Field(min_length=2, max_length=100)
    bio: str | None = Field(max_length=300)
    age: int | None = Field(ge=0, le=130)
    gender: str = Literal['male', 'female']

    model_config = ConfigDict(extra='forbid')


class NewBook(BaseModel):
    title: str
    author: str

