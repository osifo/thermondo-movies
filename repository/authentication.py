from fastapi import Depends
from sqlalchemy.orm import Session 
from config import Config
from domain.authentication.repository import IAuthenticationRepository
from domain.user.schema import User
from domain.user.model import User as UserModel
from domain.user.exceptions import UserNotFoundError
from domain.authentication.exceptions import UnauthorizedUserError
from domain.authentication.schema import UserTokenData
import services.authentication as AuthService

class AuthenticationRepository(IAuthenticationRepository):
  def __init__(self, database: Session = Depends(Config.get_database)) -> None:
    self.database = database

  async def login_user(self, email: str, password: str) -> str:
    valid_user = self.database.query(UserModel).where(UserModel.email == email).first()

    if not valid_user:
      raise UserNotFoundError
    
    verified_user = AuthService.verify_password(password, valid_user.hashed_password)
    if not verified_user:
      raise UnauthorizedUserError
    
    token_data: UserTokenData = { 'id': valid_user.id, 'firstname': valid_user.firstname, 'role': valid_user.role }
    return AuthService.generate_access_token(token_data)
    

  # TODO - to be implemented
  def logout_user(self, email: str):
    pass
  