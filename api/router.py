from fastapi import FastAPI
from sqlalchemy.orm import Session
from api.routes.v1 import movies, users, authentication
from repository.user import UserRepository
from repository.movie import MovieRepository
from repository.authentication import AuthenticationRepository
class AppRouter():
  @staticmethod
  def setup(app: FastAPI, dbConnection: Session) -> None:
    user_repo = UserRepository(database=dbConnection)
    movie_repo = MovieRepository(database=dbConnection)
    auth_repo = AuthenticationRepository(database=dbConnection, user_repository=user_repo)

    users_controller = users.controller(user_repository=user_repo, movie_repository=movie_repo) 
    movies_controller = movies.controller(repository=movie_repo)
    auth_controller = authentication.controller(auth_repository=auth_repo)

    app.include_router(users_controller)
    app.include_router(movies_controller)
    app.include_router(auth_controller)

    return app

  