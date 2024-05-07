class UserAlreadyExistsException(Exception):

    def __init__(self, message: str = "User already exists."):
        super().__init__(message)


class MaxNumberOfImagesException(Exception):

    def __init__(self, message: str = "Session reached max number of images."):
        super().__init__(message)


class SessionDoesntExistException(Exception):

    def __init__(self, message: str = "Session does not exist."):
        super().__init__(message)
