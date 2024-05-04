class AuthenticationError(Exception):
  def __init__(self, message: str = "Something went wrong while authenticating this user.", name: str = "Auth"):
        self.message = message
        self.name = name
        super().__init__(self.message, self.name)


class UnauthorizedUserError(AuthenticationError):
    """Invalid username or password"""
    pass
