from pydantic import BaseModel, EmailStr, Field

class MovieRatingCreate(BaseModel):
  user_id: str
  movie_id: str
  rating: float = Field(min=0, max=10)

class MovieRating(BaseModel):
  id: str
  movie: 'Movie'
  user_movie_rating: float = Field(min=0, max=10)

'''
HTTP Response Schema
'''
class MovieRatingResponse(BaseModel):
  success: bool
  data: MovieRating


from domain.user.schema import User
from domain.movie.schema import Movie

MovieRating.model_rebuild()
