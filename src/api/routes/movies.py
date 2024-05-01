import traceback
from fastapi import APIRouter, HTTPException, status

from domain.movie.schema import MovieListResponse, MovieResponse, MovieCreate, Movie
from domain.movie.exceptions import InvalidMovieError


def controller():
  router = APIRouter(prefix="/movies", tags=["movies"])

  @router.get("/")
  async def index(filter_params: str | None = None) -> MovieListResponse:
    try:  
      # movie_list = await repository.get_movies()
      return {
        "success": True,
        "data": "movie_list"
      }

    except InvalidMovieError as error:
        stack_trace = traceback.format_exc()
        raise HTTPException(status_code=error.code, detail=error.message)
        # self.logger.info(error.message)
    except Exception as error:
      stack_trace = traceback.format_exc()
      print(f"error:\n{error}\ndetails:{stack_trace}")
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User could not be created")


  @router.post("/")
  async def create_movie(movie_param: MovieCreate) -> MovieResponse:
    try:
      # movie = await repository.create_movie(movie=movie_param)
      return {
        "success": True,
        "data": "movie"
      }
    except InvalidMovieError as error:
      raise HTTPException(status_code=error.code, detail=error.message)
      # self.logger.info(error.message)
    except Exception as error:
      stack_trace = traceback.format_exc()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User could not be created")


  @router.get("/{movie_slug}")
  async def show_movie(movie_slug: str) -> MovieResponse:
    try:  
      # movie_data = await repository.show_movie(movie_slug)
      return {
        "success": True,
        "data": "movie_data"
      }

    except InvalidMovieError as error:
        stack_trace = traceback.format_exc()
        raise HTTPException(status_code=error.code, detail=error.message)
        # self.logger.info(error.message)
    except Exception as error:
      stack_trace = traceback.format_exc()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Movie could not be created")

  return router
