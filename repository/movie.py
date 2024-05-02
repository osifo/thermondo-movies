import bcrypt
from fastapi import Depends
from sqlalchemy.orm import Session 
from config import Config
from domain.movie.repository import IMovieRepository
from domain.movie.schema import Movie, MovieCreate
from domain.movie_rating.schema import MovieRating, MovieRatingCreate
from domain.movie.exceptions import InvalidMovieError
from domain.movie.model import Movie as MovieModel
from domain.movie_rating.model import MovieRating as MovieRatingModel


class MovieRepository(IMovieRepository):
  def __init__(self, database: Session = Depends(Config.get_database)) -> None:
    self.database = database

  async def create_movie(self, movie_params: MovieCreate) -> Movie:
    try:
      new_movie = MovieModel(**movie_params.model_dump())
      
      if not new_movie:
        raise InvalidMovieError
      
      self.database.add(new_movie)
      self.database.commit()
      self.database.refresh(new_movie)
      return new_movie
    
    except Exception as error:
      # TODO handle logging here
      raise error
  
  async def get_movie(self, movie_id: str) -> Movie:
    movie = self.database.query(MovieModel).get(movie_id)
    if not movie:
      raise InvalidMovieError
    return movie
  
  # TODO - implement pagination, ordering, filtering
  async def get_movies(self, *filter_param: object) -> list[Movie]:
    movies = self.database.query(MovieModel).order_by(MovieModel.created_at.desc()).all()
    return movies
  
  async def rate_movie(self, rating_params: MovieRatingCreate) -> MovieRating:
    try:
      with self.database.begin():
        movie_to_rate = await self.get_movie(rating_params.movie_id)
        new_rating = MovieRatingModel(**rating_params.model_dump())

        updated_movie_rating = (movie_to_rate.rating + new_rating.rating) / (movie_to_rate.reviewer_count + 1)

        self.database.add(new_rating)
        self.database.commit()
        self.database.refresh(new_rating)
        return new_rating
    except Exception as e:
        # Rollback the transaction if an error occurs
        self.database.rollback()
