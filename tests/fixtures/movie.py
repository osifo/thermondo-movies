import random
from faker import Faker
from faker.providers import date_time
from uuid import uuid4
from domain.movie.model import Movie
from sqlalchemy.orm import Session
from sqlalchemy import insert
from pytest import fixture

def movie():
  faker = Faker()
  faker.add_provider(date_time)

  title = faker.name()
  year = faker.year()
  genre = random.choice(["Action", "Drama", "Sci-fi"])
  language = random.choice(["English", "German", "French"])
  
  return {
    'title': title,
    'year': year,
    'genre': genre,
    'language': language,
    'rating': 0
  }

async def create_movie(db: Session):
  movie_model = Movie(**movie())
  db.add(movie_model)
  db.commit()
  db.refresh(movie_model)
  return movie_model

async def create_movies(db: Session, movie_count=3):
  test_movies = []

  for _ in range(movie_count):
    test_movies.append({
      **movie(), 
      'id': str(uuid4())
    })

  db.execute(insert(Movie), test_movies)
  db.commit()
  return test_movies
