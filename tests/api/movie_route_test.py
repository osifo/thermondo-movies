from fastapi.testclient import TestClient
from fastapi.responses import Response
from fastapi import status
from sqlalchemy.exc import IntegrityError
import pytest

from server import app
from tests.utils.TestBase import TestBase
from tests.fixtures.movie import (
  movie as movie_fixture,
  create_movie, 
  create_movies
) 

client = TestClient(app)

class MovieRouteTest(TestBase):
  def setUp(self) -> None:
    return super().setUp()

  async def test_create_movie(self):
    movie_params = movie_fixture()
    movie_params['title'] = "Parasite"
    movie_params['year'] = "2021"

    response = client.post("/v1/movies", json=movie_params)
    response_json = response.json()
    response_data = response_json.get('data')

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response_data.get('title'), movie_params.get('title'))
    self.assertEqual(response_data.get('year'), movie_params.get('year'))


  async def test_create_duplicate_movie(self):
    '''
    Creates a movie with duplicate title/year
    '''
    existing_movie = await create_movie(self.dbConnection)
    movie_params = movie_fixture()
    movie_params['title'] = existing_movie.title
    movie_params['year'] = existing_movie.year
    
    with self.assertRaises(IntegrityError):
      client.post("/v1/movies", json=movie_params)


  @pytest.mark.skip(reason="invalid movie")
  async def test_get_movie(self):
    test_movie = await create_movie(self.dbConnection)

    response = client.get(f"/v1/movies/{test_movie.id}")
    response_json = response.json()
    response_data = response_json.get('data')

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response_json.get("success"), True)
    self.assertEqual(response_data.get('id'), test_movie.id)
    self.assertEqual(response_data.get('title'), test_movie.title)


  async def test_get_movies(self):
    movie_count = 5
    await create_movies(self.dbConnection, movie_count=movie_count)

    response = client.get("/v1/movies")
    response_json = response.json()
    response_data = response_json.get('data')

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response_json.get('success'), True)
    self.assertGreaterEqual(len(response_data), movie_count)
  

  # TODO - write test for rating a movie
  @pytest.mark.skip(reason="to be implemented")
  async def test_rate_movie(self):
    pass

  # TODO - write test for fetching the movies a user has rated
  @pytest.mark.skip(reason="to be implemented")
  async def test_get_movie_movies(self):
    pass
