from fastapi import FastAPI
from sqlalchemy.orm import Session
from api.routes.v1 import movies, users
from repository.user import UserRepository
from repository.movie import MovieRepository
class AppRouter():
  @staticmethod
  def setup(app: FastAPI, dbConnection: Session) -> None:
    userRepo = UserRepository(database=dbConnection)
    movieRepo = MovieRepository(database=dbConnection)

    users_controller = users.controller(user_repository=userRepo, movie_repository=movieRepo) 
    movies_controller = movies.controller(repository=movieRepo) 

    app.include_router(users_controller)
    app.include_router(movies_controller)

    return app

  