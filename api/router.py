from fastapi import FastAPI
from sqlalchemy.orm import Session
from api.routes import movies, users
from repository.user import UserRepository

class AppRouter():
  @staticmethod
  def setup(app: FastAPI, dbConnection: Session) -> None:
    userRepo = UserRepository(database=dbConnection)

    users_controller = users.controller(user_repository=userRepo) 
    movies_controller = movies.controller() 

    app.include_router(users_controller)
    app.include_router(movies_controller)

    return app

  