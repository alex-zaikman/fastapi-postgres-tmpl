from typing import List

from pydantic import BaseModel, Field

from models.scopes import Scope


class _UserBase(BaseModel):
    email: str = Field(...)
    scopes: List[Scope] = Field(...)

    class Config:
        orm_mode = True


class NewUser(_UserBase):
    password: str = Field(...)

    class Config:
        orm_mode = True


class DisplayUser(_UserBase):
    id: int = Field(...)

    class Config:
        orm_mode = True


class User(NewUser, DisplayUser):
    id: int = Field(...)

    class Config:
        orm_mode = True
