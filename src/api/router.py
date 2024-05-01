from fastapi import FastAPI
from api.routes import movies, users

class AppRouter():
  @staticmethod
  def setup(app: FastAPI) -> None:
    users_controller = users.controller() 
    movies_controller = movies.controller() 

    app.include_router(users_controller)
    app.include_router(movies_controller)

    return app

  