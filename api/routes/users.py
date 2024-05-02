import traceback
from fastapi import APIRouter, HTTPException, status
from domain.user.exceptions import InvalidUserError
from domain.user.schema import (
  UserCreate, 
  User, 
  UserListResponse, 
  UserResponse, 
  UserMoviesResponse
)
from domain.user.repository import IUserRepository

def controller(user_repository: IUserRepository):
  router = APIRouter(prefix="/users", tags=["users"])

  @router.get("/")
  async def list_users(filter_params: str | None = None) -> UserListResponse:
    try:  
      user_data = await user_repository.get_users()
      return {
        "success": True,
        "data": user_data
      }

    except InvalidUserError as error:
        stack_trace = traceback.format_exc()
        print(f"error:\n{error}\ndetails:{stack_trace}")
        raise HTTPException(status_code=error.code, detail=error.message)
        # self.logger.info(error.message)
    except Exception as error:
      stack_trace = traceback.format_exc()
      print(f"error:\n{error}\ndetails:{stack_trace}")
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User could not be created")


  @router.post("/")
  async def create_user(user_param: UserCreate) -> UserResponse:
    try:
      user = await user_repository.create_user(user_params=user_param)
      return {
        "success": True,
        "data": user
      }
    except InvalidUserError as error:
      raise HTTPException(status_code=error.code, detail=error.message)
      # self.logger.info(error.message)
    except Exception as error:
      stack_trace = traceback.format_exc()
      print(f"error:\n{str(error)}")
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User could not be created")


  @router.get("/{user_id}")
  async def show_user(user_id: str) -> UserResponse:
    try:  
      user_data = await user_repository.get_user_by_id(user_id)
      return {
        "success": True,
        "data": user_data
      }

    except InvalidUserError as error:
        stack_trace = traceback.format_exc()
        raise HTTPException(status_code=error.code, detail=error.message)
        # self.logger.info(error.message)
    except Exception as error:
      stack_trace = traceback.format_exc()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User could not be created")


  @router.get("/{user_id}/movies", summary="List movies rated by a user")
  async def list_user_movies(user_id: str) -> UserMoviesResponse:
    try:
      # user_movies = await movie_repository.get_user_movies_ratings({"user_id": user_id })
      return {
        "success": True,
        "data": "user_movies"
      }

    except InvalidUserError as error:
        stack_trace = traceback.format_exc()
        print(f"error:\n{error}\ndetails:{stack_trace}")
        raise HTTPException(status_code=error.code, detail=error.message)
        # self.logger.info(error.message)
    except Exception as error:
      stack_trace = traceback.format_exc()
      print(f"error:\n{error}\ndetails:{stack_trace}")
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User could not be created")


  return router