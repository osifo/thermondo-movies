from fastapi.responses import JSONResponse
from typing import Callable
from fastapi import FastAPI, Request, status
from domain.user.exceptions import (
    UserError,
    UserNotFoundError,
    InvalidUserError,
    DuplicateUserError
)

def users_exception_handler(app: FastAPI):
    def exception_handler(
      status_code: int, exception_details: str
    ) -> Callable[[Request, UserError], JSONResponse]:
      error = exception_details

      async def handle_exception(_: Request, exc: UserError) -> JSONResponse:
        return JSONResponse(
            status_code=status_code, content={"error": error}
        )
      return handle_exception

    app.add_exception_handler(
      exc_class_or_status_code=UserNotFoundError,
      handler=exception_handler(
        status.HTTP_404_NOT_FOUND, "No matching user was found."
      )
    )

    app.add_exception_handler(
      exc_class_or_status_code=InvalidUserError,
      handler=exception_handler(
        status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid user information was supplied."
      )
    )

    app.add_exception_handler(
      exc_class_or_status_code=DuplicateUserError,
      handler=exception_handler(
          status.HTTP_400_BAD_REQUEST, "A user with this email already exists."
      )
    )
