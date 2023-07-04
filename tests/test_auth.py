# import datetime
# import datetime as dt
# import os
# import time
# import time_machine

from fastapi import status

from tests.api_base import TestAPIBase, AuthHeader


class TestAuth(TestAPIBase):

    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.headers = self.login('admin@gmail.com', 'admin123')  # pylint: disable=attribute-defined-outside-init

    async def test_auth(self):
        response = self.client.get(url='/user', headers=self.headers.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'sunny path')

        response = self.client.get(url='/user')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'no auth headers')

        response = self.client.get(url='/user', headers={"Authorization": "Bearer blasdfdfwerwewfer44r44fr44f4f4c4f4ff4f4"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, "bad auth headers")

    async def test_refresh(self):
        response = self.client.get(url='/user', headers=self.headers.refresh)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'ep with refresh')

        response = self.client.post(url='/refresh', headers=self.headers.auth)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'refresh with auth')

        response = self.client.post(url='/refresh', headers=self.headers.refresh)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'sunny path')

        new_headers = AuthHeader(response)

        response = self.client.get(url='/user', headers=new_headers.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'sunny path')

    # async def test_expiration(self):
    #
    #     with time_machine.travel(0, tick=False) as traveller:
    #         response = self.client.get(url='/user', headers=self.headers.auth)
    #         self.assertEqual(response.status_code, status.HTTP_200_OK, 'sunny path')
    #
    #         traveller.shift(datetime.timedelta(minutes=555))
    #         response = self.client.get(url='/user', headers=self.headers.auth)
    #         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'expired token')
