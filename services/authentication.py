from datetime import timedelta, datetime, timezone
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from domain.authentication.schema import UserTokenData
from config import Config

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
  return password_context.verify(plain_password, hashed_password)

def get_password_hash(password):
  return password_context.hash(password)

def generate_access_token(token_data: UserTokenData):
  expiry = datetime.now(timezone.utc) + timedelta(minutes=int(Config.AUTH_TOKEN_DURATION_MINS))
  to_encode = {**token_data,  "exp": expiry}

  return jwt.encode(to_encode, Config.AUTH_SECRET_KEY, algorithm=Config.AUTH_ALGORITHM)

   