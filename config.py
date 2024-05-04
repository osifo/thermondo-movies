import os
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import PendingRollbackError
from dotenv import load_dotenv
from enum import Enum
from typing import Literal
import logging
from logging.handlers import SysLogHandler

load_dotenv()

# TODO =  move these sections into separate files in /config dir
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
  PROJECT_NAME = os.getenv("PROJECT_NAME")
  API_VERSION = os.getenv("API_VERSION")
  PAPERTRAIL_HOST = os.getenv("PAPERTRAIL_HOST")
  PAPERTRAIL_PORT = os.getenv("PAPERTRAIL_PORT")
  PAPERTRAIL_PORT = os.getenv("PAPERTRAIL_PORT")

  # TODO - use OpenSSL implementation
  AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
  AUTH_ALGORITHM = os.getenv("AUTH_ALGORITHM")
  AUTH_TOKEN_DURATION_MINS = os.getenv("AUTH_TOKEN_DURATION_MINS")

  def __get_database_url( env: str):
    if env == Config.Environment.DEV.value:
      return URL.create(
        "mysql+pymysql",
        username=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT"),
        host=os.getenv("DB_HOST")
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

class Logger():
  @staticmethod
  def setup():
    logger = logging.getLogger(Config.PROJECT_NAME)
    logger.setLevel(logging.DEBUG)
    handler = SysLogHandler(address=(Config.PAPERTRAIL_HOST, Config.PAPERTRAIL_PORT))
    logger.addHandler(handler)

  @staticmethod
  def setup_dev():
    logging.basicConfig(
      level=logging.DEBUG,
      format="%(asctime)s %(levelname)s %(message)s",
      datefmt="%Y-%m-%d %H:%M:%S",
    )


if Config.APP_ENV == Config.Environment.DEV.value:
  Logger.setup_dev()
else:
  Logger.setup()
  