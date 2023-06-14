from typing import List

from pydantic import BaseModel, Field

from src.models.scopes import Scope


class UserBase(BaseModel):
    email: str = Field(...)
    scopes: List[Scope] = Field(...)

    class Config:
        orm_mode = True


class NewUser(UserBase):
    password: str = Field(...)

    class Config:
        orm_mode = True


class DisplayUser(UserBase):
    id: int = Field(...)

    class Config:
        orm_mode = True


class User(NewUser, DisplayUser):
    id: int = Field(...)

    class Config:
        orm_mode = True
