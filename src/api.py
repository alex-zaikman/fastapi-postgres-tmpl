import logging
from typing import List

import uvicorn
from fastapi import FastAPI, Depends

from src.database import engine, Base, get_session
from src.models import User
from src.schema import users

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/listUsers", response_model=List[User])
async def list_users(session=Depends(get_session)):
    query = users.select()
    result = await session.execute(query)
    return result.all()


if __name__ == '__main__':
    uvicorn.run("api:app",
                host="0.0.0.0",
                port=8001,
                log_level=logging.DEBUG)
