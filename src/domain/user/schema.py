from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
  firstname: str = Field(min_length=2)
  lastname: str = Field(min_length=2)
  email: EmailStr

class User(UserBase):
  id: int
  is_active: bool | None

class UserCreate(UserBase):
  password: str = Field(min_length=8, pattern='\d+\w+')
  
class UserMovies(BaseModel):
  user: User
  movies: list['MovieRating'] | None


'''
HTTP Response Schema
'''
class UserResponse(BaseModel):
  success: bool
  data: User

class UserListResponse(BaseModel):
  success: bool
  data: list[User]

  class Config:
    from_attributes = True

class UserMoviesResponse(BaseModel):
  success: bool
  data: UserMovies


from domain.movie_rating.schema import MovieRating
User.model_rebuild()
