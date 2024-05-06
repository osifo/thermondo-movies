from datetime import timedelta, datetime, timezone
from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError
from domain.authentication.schema import UserTokenData
from domain.user.model import UserRole
from domain.authentication.exceptions import (
  AuthenticationError, 
  InvalidTokenData, 
  AuthTokenExpired,
  UnauthorizedActionError
)
from domain.user.schema import UserCreate
from typing import Annotated
from fastapi import Header

from config import Config

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
  return password_context.verify(plain_password, hashed_password)

def get_password_hash(password):
  return password_context.hash(password)

# DEV-NOTE this function is private to this module
def __get_current_user(token: str):
  try:
    token_data = jwt.decode(token=token, key=Config.AUTH_SECRET_KEY)

    if not token_data:
      raise InvalidTokenData
    
    return token_data
  except  ExpiredSignatureError:
    raise AuthTokenExpired
  except JWTError as error:
    raise AuthenticationError(message=error)

def generate_access_token(token_data: UserTokenData):
  try:
    expiry = datetime.now(timezone.utc) + timedelta(minutes=int(Config.AUTH_TOKEN_DURATION_MINS))
    to_encode = {**token_data,  "exp": expiry}

    return jwt.encode(to_encode, Config.AUTH_SECRET_KEY, algorithm=Config.AUTH_ALGORITHM)
  except JWTError:
      raise AuthenticationError 
  

"""
Authentication Service Decorators
"""

def is_admin(route_handler_func):
  async def wrapper_function(user_param: UserCreate, auth_token: Annotated[str, Header()]):
    user_data: UserTokenData =__get_current_user(token=auth_token)
    if(user_data.get("role") != UserRole.Admin.value):
      raise UnauthorizedActionError
    
    return await route_handler_func(user_param=user_param)
  
  return wrapper_function
