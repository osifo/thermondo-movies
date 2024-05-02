
from fastapi import status
import json

class InvalidUserError(Exception):
  message = "The user parameters provided are invalid."
  code = status.HTTP_400_BAD_REQUEST

  def __str__(self):
    return json.dumps({
      "message": InvalidUserError.message,
      "code": InvalidUserError.code
    })
