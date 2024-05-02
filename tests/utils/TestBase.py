from unittest import IsolatedAsyncioTestCase
from sqlalchemy import Engine
from sqlalchemy.orm import scoped_session, Session
from domain.base import BaseModel

from server import databaseConfig

class TestBase(IsolatedAsyncioTestCase):
  @classmethod
  def setUpClass(cls) -> None:
    cls.Session = scoped_session(databaseConfig.session)
    cls.engine: Engine = databaseConfig.engine
    BaseModel.metadata.create_all(databaseConfig.engine)

  def setUp(self):
    self.dbConnection: Session = databaseConfig.connection

  def tearDown(self):
    self.dbConnection.rollback()
    self.dbConnection.close()

  @classmethod
  def tearDownClass(cls) -> None:
    BaseModel.metadata.drop_all(databaseConfig.engine)
    cls.Session.remove()
    cls.engine.dispose()
