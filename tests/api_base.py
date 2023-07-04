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
        from api import app  # pylint: disable=import-outside-toplevel
        self.client = TestClient(app)  # pylint: disable=attribute-defined-outside-init

    async def asyncTearDown(self) -> None:
        self.client.close()
        await super().asyncTearDown()

    def login(self, email, password) -> AuthHeader:
        response = self.client.post("/token", data={"username": email, "password": password})
        return AuthHeader(response)
