from uuid import uuid4
from datetime import datetime, timezone
from domain.base import BaseModel
from sqlalchemy import (
  Column, 
  String, 
  DateTime,
  Float,
  UniqueConstraint,
  ForeignKey
)

class MovieRating(BaseModel):
  __tablename__ = "movie_ratings"

  def __init__(self, **kwargs):
        if 'id' not in kwargs:
            kwargs['id'] = str(uuid4())
        super().__init__(**kwargs)

  id = Column(String(40), primary_key=True, index=True)
  movie_id = Column(String(40), ForeignKey("movies.id"))
  user_id = Column(String(40), ForeignKey("users.id"))
  rating = Column(Float(3,1), default=0.0, nullable=False)
  created_at = Column(DateTime(timezone=True), index=True, nullable=False, default=datetime.now(timezone.utc))
  updated_at = Column(DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc))

  __table_args__ = (
    UniqueConstraint('movie_id', 'user_id', name='unique_user_movie'),
  )
