import traceback
from fastapi import APIRouter, HTTPException, Depends, status
from domain.movie_rating.schema import MovieRatingCreate, MovieRatingResponse
from domain.movie.repository import IMovieRepository
from domain.movie.schema import (
  MovieListResponse, 
  MovieResponse, 
  MovieCreate
)


def controller(repository = Depends(IMovieRepository)):
  router = APIRouter(prefix="/v1/movies", tags=["movies"])

  @router.get("/")
  async def index(filter_params: str | None = None) -> MovieListResponse:
    movie_list = await repository.get_movies()
    return {
      "success": True,
      "data": movie_list
    }

  @router.post("/")
  async def create_movie(movie_param: MovieCreate) -> MovieResponse:
    movie = await repository.create_movie(movie_params=movie_param)
    return {
      "success": True,
      "data": movie
    }

  @router.get("/{movie_id}")
  async def show_movie(movie_id: str) -> MovieResponse:
    movie_data = await repository.get_movie(movie_id=movie_id)
    return {
      "success": True,
      "data": movie_data
    }

  @router.post("/rate")
  async def rate_movie(params: MovieRatingCreate) -> MovieRatingResponse:
    movie_rating = await repository.rate_movie(rating_params=params)
    return {
      "success": True,
      "data": movie_rating
    }

  return router
