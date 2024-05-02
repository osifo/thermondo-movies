from abc import ABC, abstractmethod
from .schema import UserCreate, User

class IUserRepository(ABC):
  @abstractmethod
  def get_users(self) -> list[User]:
    """implements fetch users"""
    raise NotImplementedError
  
  def create_user(self, user_params: UserCreate) -> User:
    """creates a new user"""
    raise NotImplementedError
  
  def get_user_by_id(self, user_id: str) -> User:
    """fetches a booking code linked to a user"""
    raise NotImplementedError