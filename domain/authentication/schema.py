from pydantic import BaseModel

class Token(BaseModel):
  access_token: str
  token_type: str

class UserLogin(BaseModel):
  email: str
  password: str

class AuthResponse(BaseModel):
  success: bool
  data: str

class UserTokenData(BaseModel):
  id: str
  firstname: str
  role: str