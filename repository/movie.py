import re
from fastapi import Depends
from sqlalchemy.orm import Session 
from sqlalchemy.exc import IntegrityError

from config import Config
from domain.movie.repository import IMovieRepository
from domain.movie.schema import Movie, MovieCreate
from domain.movie_rating.schema import MovieRating, MovieRatingCreate
from domain.movie.model import Movie as MovieModel
from domain.user.model import User as UserModel
from domain.movie_rating.model import MovieRating as MovieRatingModel
from domain.movie.exceptions import (
  InvalidMovieError, 
  MovieNotFoundError, 
  DuplicateMovieError, 
  DuplicateMovieRatingError
)


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
    
    except IntegrityError as error:
      if "duplicate entry" in str(error).lower():
        raise DuplicateMovieError
      else:
        raise error
  
  async def get_movie(self, movie_id: str) -> Movie:
    movie = self.database.query(MovieModel).get(movie_id)
    if not movie:
      raise MovieNotFoundError
    return movie
  
  # TODO - implement pagination, ordering, filtering
  async def get_movies(self, *filter_param: object) -> list[Movie]:
    movies = self.database.query(MovieModel).order_by(MovieModel.created_at.desc()).all()
    return movies
  
  # TODO - implement pagination, ordering, filtering
  async def get_movies_rated_by_user(self, user_id: str) -> list[MovieRating]:
      ratings_result = self.database.query(
        MovieModel, MovieRatingModel.rating.label("user_rating")
      ).join(
        MovieRatingModel
      ).join(
        UserModel
      ).where(
        MovieRatingModel.user_id == user_id,
        UserModel.id == user_id
      ).order_by(MovieRatingModel.created_at.desc()).all()

      movie_ratings = [dict({'movie': movie, 'user_rating': user_rating}) for movie, user_rating in ratings_result]

      return movie_ratings
  
  async def rate_movie(self, rating_params: MovieRatingCreate) -> MovieRating:
    try:
      movie_to_rate = await self.get_movie(rating_params.movie_id)
      new_rating = MovieRatingModel(**rating_params.model_dump())
      movie_to_rate.reviewer_count = int(movie_to_rate.reviewer_count) + 1
      updated_movie_rating = (int(movie_to_rate.rating) + int(new_rating.rating)) / movie_to_rate.reviewer_count
      movie_to_rate.rating = updated_movie_rating

      self.database.add(new_rating)
      self.database.commit()
      self.database.refresh(new_rating)
      self.database.refresh(movie_to_rate)

      return { 
        'user_rating': new_rating.rating, 
        'movie': movie_to_rate 
      } 
    except IntegrityError as error:
      if "duplicate entry" in str(error).lower():
        raise DuplicateMovieRatingError
      else:
        raise error