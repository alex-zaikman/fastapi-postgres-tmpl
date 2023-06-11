from pydantic import BaseModel


class User(BaseModel):
    email: str
    password: str
    id: int

    class Config:
        orm_mode = True

