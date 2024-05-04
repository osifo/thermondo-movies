from fastapi import FastAPI
from sqlalchemy.orm import Session
from api.routes.v1 import movies, users, authentication
from repository.user import UserRepository
from repository.movie import MovieRepository
from repository.authentication import AuthenticationRepository
class AppRouter():
  @staticmethod
  def setup(app: FastAPI, dbConnection: Session) -> None:
    userRepo = UserRepository(database=dbConnection)
    movieRepo = MovieRepository(database=dbConnection)
    authRepo = AuthenticationRepository(database=dbConnection)

    users_controller = users.controller(user_repository=userRepo, movie_repository=movieRepo) 
    movies_controller = movies.controller(repository=movieRepo)
    auth_controller = authentication.controller(auth_repository=authRepo)

    app.include_router(users_controller)
    app.include_router(movies_controller)
    app.include_router(auth_controller)

    return app

  