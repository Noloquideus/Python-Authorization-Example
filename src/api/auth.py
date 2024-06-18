from fastapi import APIRouter, Response
from starlette import status
from src.application.domain.user_domain import UserRegistration, UserResponse
from src.application.services.user_service import UserService

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}, 500: {"description": "Internal server error"}, 400: {"description": "Bad request"}})


@auth_router.post(
    path='/register',
    status_code=status.HTTP_201_CREATED,
    description='Register a new user by providing an email, username, and password.',
    summary='Register a new user',
    response_description='The newly registered user without the password',
    responses={
        status.HTTP_201_CREATED: {"description": "User successfully created"},
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid input data"},
        status.HTTP_409_CONFLICT: {"description": "User already exists"}})
async def register(response: Response, user_data: UserRegistration):
    user: UserResponse = await UserService.create_user(user_data)
    response.set_cookie(key="access_token", value=user.refresh_token.refresh_token, httponly=True, secure=True, samesite="strict")
    user.refresh_token.refresh_token = None
    return user
