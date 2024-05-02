from fastapi import FastAPI
from api.router import AppRouter
from config import Config, DatabaseConfig

app = FastAPI(title="Thermondo Movies API", version="1.0.0")

@app.get('/')
async def api_info():
  return {
    "success": True,
    "data": "Thermondo Movie API 1.0.0"
  }

databaseConfig: DatabaseConfig = next(Config.get_database(Config.APP_ENV))
AppRouter.setup(app, databaseConfig.connection)
