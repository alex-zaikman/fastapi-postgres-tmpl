from schema.users import users
from tests.base import TestBase


class TestSchema(TestBase):

    async def asyncSetUp(self):
        await super().asyncSetUp()
        await self.init_db()

    async def test_select_users(self):
        async with self.db.async_session.begin() as session:
            res = await session.execute(users.select())
            self.assertEqual(len(res.all()), 2)
