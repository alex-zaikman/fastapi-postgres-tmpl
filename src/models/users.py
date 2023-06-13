from typing import List

from pydantic import BaseModel, Field

from src.models.scopes import Scope


class UserBase(BaseModel):
    email: str = Field(...)
    scopes: List[Scope] = Field(...)
    id: int = Field(...)

    class Config:
        orm_mode = True


class User(UserBase):
    password: str = Field(...)

    class Config:
        orm_mode = True


class NewUser(User):
    id: int = Field(None)
    class Config:
        orm_mode = True
