from pydantic import BaseModel, EmailStr, Field
from typing import Literal

class MovieCreate(BaseModel):
  title: str = Field(min_length=2)
  year: str = Field(length=4)
  genre: str
  runtime: str
  language: str | None
  year: str
  thumbnail_url: str | None
  rating: float

class Movie(MovieCreate):
  id: str
  slug: str
  

'''
HTTP Response Schema
'''
class MovieResponse(BaseModel):
  success: bool
  data: Movie

class MovieListResponse(BaseModel):
  success: bool
  data: list[Movie]

  class Config:
    from_attributes = True

