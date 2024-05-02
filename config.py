import os
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.event import listen
from dotenv import load_dotenv
from enum import Enum
from typing import Literal

load_dotenv()

class DatabaseConfig():
  def __init__(self, connection, session, engine) -> None:
    self.connection = connection
    self.session = session
    self.engine = engine

class Config:
  APP_ENV = os.getenv("APP_ENV")
  Environment = Enum('Environment', {
    'TEST': 'test', 
    'DEV': 'development', 
    'STAGING': 'staging', 
    'PROD': 'production'
  })

  def __get_database_url( env: str):
    if env == Config.Environment.DEV.value:
      return URL.create(
        "mysql+pymysql",
        username=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT")
      )
    if env == Config.Environment.TEST.value:
      return 'sqlite:///./movies_test.db'

  @staticmethod
  def get_database(env: Literal['test', 'development', 'staging', 'production']):
    db_url = Config.__get_database_url(env)
    db_engine = create_engine(db_url)
      
    DBSession = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    db_connection = DBSession()

    try:
      yield DatabaseConfig(db_connection, DBSession, db_engine) 
    finally:
      db_connection.close()

