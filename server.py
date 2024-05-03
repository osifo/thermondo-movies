from fastapi import FastAPI
from api.router import AppRouter
from api.exceptions import AppException
from config import Config, DatabaseConfig

app = FastAPI(title=Config.PROJECT_NAME, version=Config.API_VERSION)

@app.get('/')
async def __api_info():
  return {
    "success": True,
    "data": f"{Config.PROJECT_NAME} - {Config.API_VERSION}"
  }

databaseConfig: DatabaseConfig = next(Config.get_database(Config.APP_ENV))

AppRouter.setup(app, databaseConfig.connection)
AppException.setup(app)
