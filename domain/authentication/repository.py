from abc import ABC, abstractmethod
from domain.user.schema import User

class IAuthenticationRepository(ABC):
  @abstractmethod
  def login_user(self, email: str, password: str) -> User:
    """Login user"""
    raise NotImplementedError
  
  @abstractmethod
  def logout_user(self, email: str):
    """Logout user"""
    raise NotImplementedError
  