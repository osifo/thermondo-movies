class MovieError(Exception):
  def __init__(self, message: str = "Something went wrong while performing a movie operation.", name: str = "Movies"):
        self.message = message
        self.name = name
        super().__init__(self.message, self.name)


class DuplicateMovieError(MovieError):
    """A movie with same title and year already exists."""
    pass

class InvalidMovieError(MovieError):
    """Invalid movie information was supplied."""
    pass

class MovieNotFoundError(MovieError):
    """No matching movie was found."""
    pass

class DuplicateMovieRatingError(MovieError):
    """You have rated this movie previously."""
    pass