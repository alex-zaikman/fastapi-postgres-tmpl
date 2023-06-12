from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class Scope(str, Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'


class TokenType(str, Enum):
    ACCESS = 'ACCESS'
    REFRESH = 'REFRESH'


class Token(BaseModel):
    """jwt token"""
    access_token: str = Field(...)
    refresh_token: str = Field(...)
    token_type: str = Field(...)


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


class TokenData(BaseModel):
    """jwt token"""
    exp: int = Field(...)
    user: User = Field(...)
