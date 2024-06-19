from fastapi import APIRouter, Response
from starlette import status
from src.application.domain.user_domain import UserRegistration, UserResponse, UserDto
from src.application.services.user_service import UserService
from src.infrastructure.utils.token_service import TokenService

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
    response.set_cookie(key="refresh_token", value=user.refresh_token.refresh_token, httponly=True, secure=True, samesite="strict")
    user.refresh_token.refresh_token = None
    return user


@auth_router.get(
    path='/verify',
    status_code=status.HTTP_200_OK,
    description='Verify email address using the provided token.',
    summary='Verify email address',
    response_description='Email verification status',
    responses={
        status.HTTP_200_OK: {"description": "Email successfully verified"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid or expired token"},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"}})
async def verify(token: str):
    return UserService.verify_user(token)
