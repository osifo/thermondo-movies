from datetime import timedelta, datetime, timezone
from passlib.context import CryptContext
from jose import jwt, JWTError
from domain.authentication.schema import UserTokenData
from domain.authentication.exceptions import AuthenticationError, InvalidTokenData, AuthTokenExpired
from config import Config

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
  return password_context.verify(plain_password, hashed_password)

def get_password_hash(password):
  return password_context.hash(password)

def get_current_user(token: str):
  try:
    token_data = jwt.decode(token=token, key=Config.AUTH_SECRET_KEY)

    if not token_data:
      raise InvalidTokenData

    current_time = int(datetime.now(timezone.utc).timestamp())
    token_expiry_time = int(token_data.get("exp"))
    if token_expiry_time < current_time:
      raise AuthTokenExpired
    
    return token_data
    
  except JWTError:
    raise AuthenticationError 

def generate_access_token(token_data: UserTokenData):
  try:
    expiry = datetime.now(timezone.utc) + timedelta(minutes=int(Config.AUTH_TOKEN_DURATION_MINS))
    to_encode = {**token_data,  "exp": expiry}

    return jwt.encode(to_encode, Config.AUTH_SECRET_KEY, algorithm=Config.AUTH_ALGORITHM)
  except JWTError:
      raise AuthenticationError 


   