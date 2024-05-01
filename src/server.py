from fastapi import FastAPI

import sys; 
print("===================")
print(sys.path)

from api.router import AppRouter

app = FastAPI()

@app.get('/')
async def api_info():
  return {
    "success": True,
    "data": "Thermondo Movie API 1.0.0"
  }

AppRouter.setup(app)
