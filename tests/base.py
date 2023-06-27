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
        # os.environ.setdefault('DB_NULL_POOL', 'true')
        os.environ.setdefault('DB_ECHO', 'true')
        self.db = DataBase()  # pylint: disable=attribute-defined-outside-init

    async def init_db(self):
        await super().asyncSetUp()
        session = await anext(self.db.get_session())
        with open('../db/init.sql', 'r') as fp:
            _ = [(await session.execute(text(statment.strip()))) for statment in fp.read().split(';') if statment.strip()]
            await session.commit()

    async def asyncTearDown(self) -> None:
        self.postgresql.stop()
