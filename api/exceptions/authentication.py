import logging, traceback
from fastapi.responses import JSONResponse
from typing import Callable
from fastapi import FastAPI, Request, status
from domain.authentication.exceptions import (
  AuthenticationError, 
  UnauthorizedUserError, 
  InvalidTokenData,
  AuthTokenExpired,
)


def auth_exception_handler(app: FastAPI):
  logger = logging.getLogger(__name__)

  def exception_handler(
      status_code: int, exception_details: str
  ) -> Callable[[Request, AuthenticationError], JSONResponse]:
    error = exception_details
    
    async def handle_exception(request: Request, exc: AuthenticationError) -> JSONResponse:
      stack_trace = traceback.format_exc(limit=1)
      logger.debug(error)
      logger.error(stack_trace)
      
      return JSONResponse(
          status_code=status_code, content={"error": error}
      )
    return handle_exception

  app.add_exception_handler(
    exc_class_or_status_code = UnauthorizedUserError,
    handler = exception_handler(
        status.HTTP_401_UNAUTHORIZED, "Incorrect email or password"
    )
  )

  app.add_exception_handler(
    exc_class_or_status_code = InvalidTokenData,
    handler = exception_handler(
        status.HTTP_401_UNAUTHORIZED, "Invalid token data."
    )
  )
  app.add_exception_handler(
    exc_class_or_status_code = AuthTokenExpired,
    handler = exception_handler(
        status.HTTP_401_UNAUTHORIZED, "Authentication token has expired."
    )
  )
