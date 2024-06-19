from fastapi import HTTPException, status


class DefaultException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class UserAlreadyExistsException(DefaultException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail="User with this email or username already exists")