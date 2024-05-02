import traceback
from fastapi import APIRouter, HTTPException, Depends, status
from domain.movie_rating.schema import MovieRatingCreate, MovieRatingResponse
from domain.movie.exceptions import InvalidMovieError
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
    try:  
      movie_list = await repository.get_movies()
      return {
        "success": True,
        "data": movie_list
      }

    except InvalidMovieError as error:
        stack_trace = traceback.format_exc()
        raise HTTPException(status_code=error.code, detail=error.message)
        # self.logger.info(error.message)
    except Exception as error:
      stack_trace = traceback.format_exc()
      print(error)
      print(f"error:\n{error}\ndetails:{stack_trace}")
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Movie could not be fetched")


  @router.post("/")
  async def create_movie(movie_param: MovieCreate) -> MovieResponse:
    try:
      movie = await repository.create_movie(movie_params=movie_param)
      return {
        "success": True,
        "data": movie
      }
    except InvalidMovieError as error:
      raise HTTPException(status_code=error.code, detail=error.message)
      # self.logger.info(error.message)
    except Exception as error:
      stack_trace = traceback.format_exc()
      print(error)
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Movie could not be created")


  @router.get("/{movie_id}")
  async def show_movie(movie_id: str) -> MovieResponse:
    try:  
      movie_data = await repository.get_movie(movie_id=movie_id)
      return {
        "success": True,
        "data": movie_data
      }

    except InvalidMovieError as error:
        stack_trace = traceback.format_exc()
        raise HTTPException(status_code=error.code, detail=error.message)
        # self.logger.info(error.message)
    except Exception as error:
      stack_trace = traceback.format_exc()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Movie could not be created")
    

  @router.post("/rate")
  async def rate_movie(params: MovieRatingCreate) -> MovieRatingResponse:
    try:
      
      movie_rating = await repository.rate_movie(rating_params=params)
      return {
        "success": True,
        "data": movie_rating
      }

    except InvalidMovieError as error:
        stack_trace = traceback.format_exc()
        raise HTTPException(status_code=error.code, detail=error.message)
        # self.logger.info(error.message)
    except Exception as error:
      stack_trace = traceback.format_exc()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Movie could not be created")

  return router
