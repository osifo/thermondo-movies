from fastapi.testclient import TestClient
from fastapi.responses import Response
from fastapi import status
import unittest

from server import app
from tests.utils.TestBase import TestBase
from tests.fixtures.user import (
  user as user_fixture,
  create_user, 
  create_users
) 

client = TestClient(app)

class UserRouteTest(TestBase):
  def setUp(self) -> None:
    return super().setUp()

  async def test_create_user(self):
    user_params = user_fixture()
    user_params['email'] = "testuser@gmail.com"
    user_params['password'] = "TESTpassword"

    response = client.post("/v1/users", json=user_params)
    response_json = response.json()
    response_data = response_json.get('data')

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response_data.get('email'), user_params.get('email'))
    self.assertEqual(response_data.get('firstname'), user_params.get('firstname'))
    self.assertEqual(response_data.get('lastname'), user_params.get('lastname'))

  async def test_create_user_invalid_email(self):
    user_params = user_fixture()
    user_params['email'] = "testusergmail@"
    user_params['email'] = "TEST2password"

    response = client.post("/v1/users", json=user_params)
    response_json = response.json()

    self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)


  async def test_get_user(self):
    test_user = await create_user(self.dbConnection)

    response = client.get(f"/v1/users/{test_user.id}")
    response_json = response.json()
    response_data = response_json.get('data')

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response_json.get("success"), True)
    self.assertEqual(response_data.get('id'), test_user.id)
    self.assertEqual(response_data.get('email'), test_user.email)

  async def test_get_users(self):
    user_count = 5
    await create_users(self.dbConnection, user_count=user_count)

    response = client.get("/v1/users")
    response_json = response.json()
    response_data = response_json.get('data')

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response_json.get('success'), True)
    self.assertGreaterEqual(len(response_data), user_count)
  
  
  @unittest.skip("to be implemented")  # TODO - write test for rating a movie
  async def test_rate_movie(self):
    pass

  @unittest.skip("to be implemented") # TODO - write test for fetching user movies 
  async def test_get_user_movies(self):
    pass
