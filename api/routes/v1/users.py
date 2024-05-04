from fastapi import APIRouter, Depends
from domain.user.repository import IUserRepository
from domain.movie.repository import IMovieRepository
from domain.user.schema import (
  UserCreate, 
  UserListResponse, 
  UserResponse, 
  UserMoviesResponse
)

def controller(user_repository = Depends(IUserRepository),  movie_repository = Depends(IMovieRepository)):
  router = APIRouter(prefix="/v1/users", tags=["users"])

  # TODO - implement pagination and filtering 
  @router.get("/")
  async def list_users(filter_params: str | None = None) -> UserListResponse:
    user_data = await user_repository.get_users()
    return {
      "success": True,
      "data": user_data
    }
  
  @router.post("/")
  async def create_user(user_param: UserCreate) -> UserResponse:
    user = await user_repository.create_user(user_params=user_param)
    return {
      "success": True,
      "data": user
    }

  @router.get("/{user_id}")
  async def show_user(user_id: str) -> UserResponse:
    user_data = await user_repository.get_user_by_id(user_id)
    return {
      "success": True,
      "data": user_data
    }

  @router.get("/{user_id}/movies", summary="List movies rated by a user")
  async def list_user_movies(user_id: str) -> UserMoviesResponse:
    user = await user_repository.get_user_by_id(user_id)
    user_movies = await movie_repository.get_movies_rated_by_user(user_id)

    return {
      "success": True,
      "data": { 'user': user, 'movies': user_movies }
    }

  return router