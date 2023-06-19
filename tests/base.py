import unittest
import testing.postgresql

from fastapi.openapi.models import Response
from starlette.testclient import TestClient
from database import DataBase


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


class TestBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.postgresql = testing.postgresql.Postgresql()
        cls.postgresql.initialize()
        DataBase(sqlalchemy_database_url=cls.postgresql.url().replace('postgresql:', 'postgresql+asyncpg:'))


    def setUp(self) -> None:
        from api import app
        self.client = TestClient(app)

    def login(self, email, password) -> AuthHeader:
        response = self.client.post("/token", data={"username": email, "password": password})
        return AuthHeader(response)

    def tearDown(self):
        self.postgresql.stop()
