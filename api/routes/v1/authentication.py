from fastapi import APIRouter, Depends
from domain.authentication.repository import IAuthenticationRepository
from domain.authentication.schema import UserLogin, AuthResponse
from domain.user.schema import UserCreate
def controller(auth_repository = Depends(IAuthenticationRepository)):
  router = APIRouter(prefix="/v1/auth", tags=["authentication"])

  @router.post('/signup')
  async def signup(user_params: UserCreate) -> AuthResponse:
    return {
      "success": True,
      "data": "data"
    }
  
  @router.post('/login')
  async def login(auth_param: UserLogin) -> AuthResponse:
    user_token = await auth_repository.login_user(email=auth_param.email, password=auth_param.password)
    return {
      "success": True,
      "data": user_token
    }
  
  # TODO - implement login via swagger docs
  # @router.post('/api__login')
  # def generate_access_token(form_data):
  # pass

  # TODO - implement logout route
  @router.post('/logout')
  async def logout():
    return {
      "success": True,
      "data": "not yet implemented"
    }
  

  return router

