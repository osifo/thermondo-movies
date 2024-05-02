from uuid import uuid4
from datetime import datetime, timezone
from domain.base import BaseModel
from sqlalchemy import (
  Column, 
  String, 
  Boolean, 
  Float,
  Integer,
  DateTime,
  UniqueConstraint
)

class Movie(BaseModel):
  __tablename__ = "movies"

  def __init__(self, **kwargs):
    if 'id' not in kwargs:
        kwargs['id'] = str(uuid4())
    super().__init__(**kwargs)

  id = Column(String(40), primary_key=True, index=True)
  title = Column(String(255), unique=True, index=True, nullable=False)
  year = Column(String(255))
  genre = Column(String(255))
  duration_mins = Column(Integer)
  language = Column(String(255))
  thumbnail_url = Column(String(255))
  rating = Column(Float(3,1), default=0.0, nullable=False)
  reviewer_count = Column(Integer, default=0, nullable=False)
  is_active = Column(Boolean)
  created_at = Column(DateTime(timezone=True), index=True, nullable=False, default=datetime.now(timezone.utc))
  updated_at = Column(DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc))
  
  __table_args__ = (
    UniqueConstraint('title', 'year', name='unique_title_year'),
  )
