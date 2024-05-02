import bcrypt
from fastapi import Depends
from sqlalchemy.orm import Session 
from config import Config
from domain.user.repository import IUserRepository
from domain.user.schema import User , UserCreate, UserMovies
from domain.user.exceptions import InvalidUserError
from domain.user.model import User as UserModel
from domain.movie_rating.schema import MovieRating


class UserRepository(IUserRepository):
  def __init__(self, database: Session = Depends(Config.get_database)) -> None:
    self.database = database

  async def create_user(self, user_params: UserCreate) -> User:
    try:
      hashed_password = bcrypt.hashpw(user_params.password.encode('utf-8'), bcrypt.gensalt())
      new_user = UserModel(
        **user_params.model_dump(exclude=['password']), 
        hashed_password=hashed_password
      )
      
      if not new_user:
        raise InvalidUserError
      
      self.database.add(new_user)
      self.database.commit()
      self.database.refresh(new_user)
      return new_user
    
    except Exception as error:
      # handle logging here
      raise error
  
  async def get_user_by_id(self, user_id: str) -> User:
    user = self.database.query(UserModel).get(user_id)
    if not user:
      raise InvalidUserError
    return user
  
  # TODO - implement pagination, ordering, filtering
  async def get_users(self, *filter_param: object) -> list[User]:
    users = self.database.query(UserModel).order_by(UserModel.created_at.desc()).all()
    return users
  