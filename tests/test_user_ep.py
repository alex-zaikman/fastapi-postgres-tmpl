from tests.api_base import TestAPIBase


class TestUserEP(TestAPIBase):

    async def test_crud_users(self):

        headers = self.login('admin@gmail.com', 'admin123')
        self.client.post(
            url='/user',
            headers=headers.auth,
            json={
                "email": "string",
                "scopes": [
                    "ADMIN"
                ],
                "password": "string"
            }
        )
        sss = 21
