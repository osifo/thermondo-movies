from fastapi import APIRouter, Depends
from domain.authentication.repository import IAuthenticationRepository
from domain.authentication.schema import UserLogin, AuthResponse
from domain.user.schema import UserCreate

def controller(auth_repository = Depends(IAuthenticationRepository)):
  router = APIRouter(prefix="/v1/auth", tags=["authentication"])

  @router.post('/signup')
  async def signup(user_param: UserCreate) -> AuthResponse:
    user_token = await auth_repository.signup_user(user=user_param)
    return {
      "success": True,
      "data": user_token
    }
  
  @router.post('/login')
  async def login(auth_param: UserLogin) -> AuthResponse:
    user_token = await auth_repository.login_user(email=auth_param.email, password=auth_param.password)
    return {
      "success": True,
      "data": user_token
    }
  
  # TODO - implement login via swagger doc

  return router

