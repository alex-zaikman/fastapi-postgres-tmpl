from __future__ import annotations

import os

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DB_HOST = os.environ.get('DB_HOST', default='localhost')
DB_PORT = os.environ.get('DB_PORT', default='5432')
DB_USER = os.environ.get('DB_USER', default='postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', default='postgres')
DB_NAME = os.environ.get('DB_NAME', default='postgres')

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        except:
            await session.rollback()
        else:
            await session.commit()
        finally:
            await session.close()