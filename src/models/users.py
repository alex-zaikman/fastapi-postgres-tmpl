from typing import List

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str = Field(...)
    id: int = Field(...)
    scopes: List[str] = Field(...)

    class Config:
        orm_mode = True


class User(UserBase):
    password: str = Field(...)

    class Config:
        orm_mode = True
