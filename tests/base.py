import unittest

from database import DataBase
from tests.mock_db import Postgresql


class TestBase(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.postgresql = Postgresql()

    async def asyncSetUp(self):
        self.db = DataBase(self.postgresql.url().replace('postgresql', 'postgresql+asyncpg'))  # pylint: disable=attribute-defined-outside-init

    @classmethod
    def tearDownClass(cls) -> None:
        Postgresql.clear_cache()
