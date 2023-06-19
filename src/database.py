from __future__ import annotations

import os

from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from singleton_meta import SingletonMeta


class DataBase(metaclass=SingletonMeta):

    def __init__(self, sqlalchemy_database_url):
        if sqlalchemy_database_url is None:
            db_host = os.environ.get('DB_HOST', default='localhost')
            db_port = os.environ.get('DB_PORT', default='5432')
            db_user = os.environ.get('DB_USER', default='postgres')
            db_password = os.environ.get('DB_PASSWORD', default='postgres')
            db_name = os.environ.get('DB_NAME', default='postgres')
            sqlalchemy_database_url = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        self.engine = create_async_engine(
            sqlalchemy_database_url,
            echo=True
        )

        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

        self._create_all()

    def _create_all(self):
        conn = self.engine.connect()
        conn.run_sync(self.Base.metadata.create_all)

    async def get_session(self) -> AsyncSession:
        async with self.async_session() as session:
            async with session.begin():
                try:
                    yield session
                except:  # pylint: disable=bare-except
                    await session.rollback()

    class Base(AsyncAttrs, DeclarativeBase):
        pass
