from fastapi.openapi.models import Response
from fastapi.testclient import TestClient

from tests.base import TestBase


class AuthHeader:
    def __init__(self, response: Response):
        self._tokens = response.json()
        self.status_code = response.status_code

    @property
    def auth(self):
        return {"Authorization": f"Bearer {self._tokens.get('access_token')}"}

    @property
    def refresh(self):
        return {"Authorization": f"Bearer {self._tokens.get('refresh_token')}"}


class TestAPIBase(TestBase):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        await self.init_db()
        from api import app
        self.client = TestClient(app)

    def login(self, email, password) -> AuthHeader:
        response = self.client.post("/token", data={"username": email, "password": password})
        return AuthHeader(response)
