from abc import ABC, abstractmethod
from .schema import MovieCreate, Movie
from domain.movie_rating.schema import MovieRatingCreate, MovieRating

class IMovieRepository(ABC):
  @abstractmethod
  def get_movies(self) -> list[Movie]:
    """fetch movie list"""
    raise NotImplementedError
  
  def get_movie(self, movie_id: str) -> Movie:
    """fetch movie details"""
    raise NotImplementedError
  
  def create_movie(self, movie: MovieCreate) -> Movie:
    """creates a new movie"""
    raise NotImplementedError
  
  def rate_movie(self, rating_params: MovieRatingCreate) -> MovieRating:
    """fetch movie details"""
    raise NotImplementedError