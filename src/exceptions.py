from fastapi import HTTPException, status


class DefaultException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class UserAlreadyExistsException(DefaultException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail="User with this email or username already exists")


class TokenTimeIsExpiredException(DefaultException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token time is expired")


class InvalidTokenException(DefaultException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


class UserNotFoundException(DefaultException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


class UserNotFoundByEmailException(DefaultException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="User not found by email")


class UserNotFoundByUsernameException(DefaultException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="User not found by username")


class InvalidCredentialsException(DefaultException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
