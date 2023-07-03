from __future__ import annotations

import os

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from singleton_meta import SingletonMeta


class DataBase(metaclass=SingletonMeta):

    def __init__(self):

        self.engine = self._create_async_engine()

        self.async_session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    @staticmethod
    def _create_async_engine():
        db_host = os.environ.get('DB_HOST', default='localhost')
        db_port = os.environ.get('DB_PORT', default='5432')
        db_user = os.environ.get('DB_USER', default='postgres')
        db_password = os.environ.get('DB_PASSWORD', default='postgres')
        db_name = os.environ.get('DB_NAME', default='postgres')
        kwargs = dict(url=f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
        if os.environ.get('DB_NULL_POOL', default=None) is not None:
            kwargs.update(poolclass=NullPool)
        if os.environ.get('DB_ECHO', default=None) is not None:
            kwargs.update(echo=True)
        return create_async_engine(
            **kwargs
        )

    async def get_session(self) -> AsyncSession:
        async with self.async_session() as session:
            async with session.begin():
                try:
                    yield session
                except Exception as exc:  # pylint: disable=bare-except
                    await session.rollback()
                    raise exc
                else:
                    await session.commit()
                finally:
                    await session.close()

    class Base(AsyncAttrs, DeclarativeBase):
        pass
