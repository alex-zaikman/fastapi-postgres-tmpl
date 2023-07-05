from fastapi import status
from tests.api_base import TestAPIBase


class TestUserEP(TestAPIBase):

    def test_ping(self):
        response = self.client.get(url='/ping')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crud_users(self):
        headers = self.login('admin@gmail.com', 'admin123')
        response = self.client.post(
            url='/user',
            headers=headers.auth,
            json={
                "email": "test@test.com",
                "scopes": [
                    "ADMIN"
                ],
                "password": "test123"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        res = self.login('test@test.com', 'test123')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
