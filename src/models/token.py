from enum import Enum

from pydantic import BaseModel, Field

from models.users import User


class TokenType(str, Enum):
    ACCESS = 'ACCESS'
    REFRESH = 'REFRESH'


class Token(BaseModel):
    """jwt token"""
    access_token: str = Field(...)
    refresh_token: str = Field(...)
    token_type: str = Field(...)


class TokenData(BaseModel):
    """jwt token"""
    exp: int = Field(...)
    user: User = Field(...)
