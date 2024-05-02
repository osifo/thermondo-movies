import os
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import PendingRollbackError
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
    
    if env == Config.Environment.TEST.value:
      db_engine = create_engine(db_url, connect_args={"check_same_thread": False}) # because i'm using sqlite
    else:
      db_engine = create_engine(db_url)
      
    DBSession = sessionmaker(autocommit=False, autoflush=True, bind=db_engine)
    db_connection = DBSession()

    # TODO - Fix bug with PendingRollbackError
    try:
      yield DatabaseConfig(db_connection, DBSession, db_engine)
    except PendingRollbackError as error:
      db_connection.rollback()
      raise error
    except Exception as error:
      db_connection.rollback()
      raise error
    finally:
      db_connection.close()

