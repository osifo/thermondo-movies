from pydantic import BaseModel, Field

class MovieCreate(BaseModel):
  title: str = Field(min_length=2)
  year: str = Field(length=4)
  genre: str
  duration_mins: int
  language: str | None
  thumbnail_url: str | None = Field(None)
  rating: float = Field(0.0, ge=0.0, le=10.0)

class Movie(MovieCreate):
  id: str
  reviewer_count: int = Field(..., exclude=True)

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
