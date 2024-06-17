from typing import Optional, List

from pydantic import EmailStr, BaseModel, Field, StrictStr


class UserRegistration(BaseModel):
    email: EmailStr = Field(title='Email',
                            description='The email of the user',
                            examples=['example@example.com', 'example1@example.com', 'example2@example.com'])

    username: StrictStr = Field(title='Username',
                                description='The username of the user',
                                min_length=3,
                                max_length=30,
                                examples=['username', 'username1', 'username2'])

    password: StrictStr = Field(title='Password',
                                description='The password of the user',
                                min_length=8,
                                max_length=64,
                                examples=['password', 'password1', 'password2'])


class UserData(BaseModel):
    email: str
    username: str
    password_hash: str


class UserDto(BaseModel):
    id: Optional[int] = None
    email: Optional[str] = None
    username: Optional[str] = None
    is_email_verified: Optional[bool] = None
    refresh_tokens: Optional[List[str]] = None
