import logging

import uvicorn
from fastapi import FastAPI, Depends

from src.database import engine, Base
from src.models import users

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "Hello World"}

def get_session():
    async with async_session() as session:
        async with session.begin():
            yield session


@app.get("/listUsers")
async def list_users(database=Depends()):
    query = users.select()
    return await database.fetch_all(query)


if __name__ == '__main__':
    uvicorn.run("api:app",
                host="0.0.0.0",
                port=8000,
                log_level=logging.DEBUG)
