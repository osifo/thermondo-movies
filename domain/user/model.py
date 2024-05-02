from uuid import uuid4
from enum import Enum
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from domain.base import BaseModel

class UserRole(Enum):
  Basic='basic'
  Admin='admin'

class User(BaseModel):
  __tablename__ = "users"

  def __init__(self, **kwargs):
      if 'id' not in kwargs:
          kwargs['id'] = str(uuid4())
      super().__init__(**kwargs)

  id = Column(String(40), primary_key=True, index=True)
  email = Column(String(255), unique=True, index=True, nullable=False)
  firstname = Column(String(255))
  lastname = Column(String(255))
  hashed_password = Column(String(255))
  role = Column(String(255), default=UserRole.Basic.value)
  is_active = Column(Boolean, default=True)
  created_at = Column(DateTime(timezone=True), index=True, nullable=False, default=datetime.now(timezone.utc))
  updated_at = Column(DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc))
  
  rated_movies = relationship("Movie", secondary="movie_ratings", viewonly=True, order_by="MovieRating.created_at.desc()")
