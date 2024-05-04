import re, logging, traceback
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from .movie import movies_exception_handler
from .user import users_exception_handler
from .authentication import auth_exception_handler

class AppException():
  @staticmethod
  def setup(app: FastAPI) -> None:
    logger = logging.getLogger(__name__)

    movies_exception_handler(app)
    users_exception_handler(app)
    auth_exception_handler(app)

    # TODO - Write custom handler for HTTPException (to handle 500s)

    @app.exception_handler(RequestValidationError)
    async def validate_exception_handler(request: Request, exception: str):
      validation_errors = []
      exception = exception.args[0]

      for error in exception:
        error_field = error['loc'][1] 
        error_message = str(error['msg']).lower()
        formatted_error = re.sub(r'^(\w+)\s-\s(\w+)\s+(\w+\s+)', r'\1 \3', f"{error_field} - {error_message}")
        validation_errors.append(formatted_error)

      formatted_error_message = ", ".join(validation_errors)
      stack_trace = traceback.format_exc(limit=1)

      logger.debug(formatted_error_message)
      logger.error(stack_trace)

      return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={ "error": formatted_error_message }
      )

  