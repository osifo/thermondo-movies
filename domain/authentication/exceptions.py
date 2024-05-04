class AuthenticationError(Exception):
  def __init__(self, message: str = "Something went wrong while authenticating this user.", name: str = "Auth"):
        self.message = message
        self.name = name
        super().__init__(self.message, self.name)


class UnauthorizedUserError(AuthenticationError):
    """Invalid username or password"""
    pass
class InvalidTokenData(AuthenticationError):
    """Invalid token data"""
    pass
class AuthTokenExpired(AuthenticationError):
    """Authentication token has expired."""
    pass
