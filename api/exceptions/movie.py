import logging, traceback
from fastapi.responses import JSONResponse
from typing import Callable
from fastapi import FastAPI, Request, status
from domain.movie.exceptions import (
    MovieError,
    MovieNotFoundError,
    InvalidMovieError,
    DuplicateMovieError,
    DuplicateMovieRatingError
)


def movies_exception_handler(app: FastAPI):
  logger = logging.getLogger(__name__)

  def exception_handler(
      status_code: int, exception_details: str
  ) -> Callable[[Request, MovieError], JSONResponse]:
    error = exception_details
    
    async def handle_exception(request: Request, exc: MovieError) -> JSONResponse:
      stack_trace = traceback.format_exc(limit=1)
      logger.debug(error)
      logger.error(stack_trace)
      
      return JSONResponse(
          status_code=status_code, content={"error": error}
      )
    return handle_exception

  app.add_exception_handler(
    exc_class_or_status_code = MovieNotFoundError,
    handler = exception_handler(
        status.HTTP_404_NOT_FOUND, "No matching movie was found."
    )
  )

  app.add_exception_handler(
    exc_class_or_status_code = InvalidMovieError,
    handler = exception_handler(
        status.HTTP_400_BAD_REQUEST, "Invalid movie information was supplied."
    )
  )

  app.add_exception_handler(
    exc_class_or_status_code = DuplicateMovieError,
    handler = exception_handler(
        status.HTTP_400_BAD_REQUEST, "A movie with this name and year already exists."
    )
  )

  app.add_exception_handler(
    exc_class_or_status_code = DuplicateMovieRatingError,
    handler = exception_handler(
        status.HTTP_400_BAD_REQUEST, "You have rated this movie previously."
    )
  )
