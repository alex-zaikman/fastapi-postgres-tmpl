import os
import unittest

import testing.postgresql
from sqlalchemy import text

from database import DataBase


class TestBase(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.postgresql = testing.postgresql.Postgresql()  # pylint: disable=attribute-defined-outside-init
        dsn = self.postgresql.dsn()
        os.environ.setdefault('DB_HOST', dsn['host'])
        os.environ.setdefault('DB_PORT', str(dsn['port']))
        os.environ.setdefault('DB_USER', dsn['user'])
        os.environ.setdefault('DB_PASSWORD', '')
        os.environ.setdefault('DB_NAME', 'postgres')
        os.environ.setdefault('DB_NULL_POOL', 'true')
        os.environ.setdefault('DB_ECHO', 'true')
        self.db = DataBase()  # pylint: disable=attribute-defined-outside-init

    # async def asyncTearDown(self) -> None:
    #     # self.db.async_session.close_all()
    #     self.db.engine.dispose()
    #     self.postgresql.stop()

    async def init_db(self):
        await super().asyncSetUp()
        async with self.db.async_session.begin() as session:
            with open('../db/init.sql', 'r') as fp:
                _ = [(await session.execute(text(statement.strip()))) for statement in fp.read().split(';') if statement.strip()]
            await session.commit()
            await session.close()
