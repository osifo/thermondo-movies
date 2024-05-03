class UserError(Exception):
  def __init__(self, message: str = "Something went wrong while performing this user operation.", name: str = "Users"):
        self.message = message
        self.name = name
        super().__init__(self.message, self.name)


class DuplicateUserError(UserError):
    """A user with this email already exists."""
    pass

class InvalidUserError(UserError):
    """Invalid user information was supplied."""
    pass

class UserNotFoundError(UserError):
    """No matching user was found."""
    pass