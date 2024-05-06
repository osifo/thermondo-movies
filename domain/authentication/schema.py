from pydantic import BaseModel
from domain.user.schema import User

class Token(BaseModel):
  access_token: str
  token_type: str

class UserLogin(BaseModel):
  email: str
  password: str

class UserSignup(BaseModel):
  user: User
  auth_token: str

class AuthResponse(BaseModel):
  success: bool
  data: str
class SignupResponse(BaseModel):
  success: bool
  data: UserSignup

class UserTokenData(BaseModel):
  id: str
  firstname: str
  role: str