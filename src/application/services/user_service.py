from uuid import UUID
from src.application.domain.jwt import RefreshToken, AccessToken
from src.application.domain.user_domain import UserRegistration, UserData, UserDto, UserResponse, UserLogin
from src.config import settings
from src.exceptions import UserNotFoundByEmailException, UserNotFoundException, InvalidCredentialsException, TooManyRefreshTokensException
from src.infrastructure.database.models import User
from src.infrastructure.database.repositories.user_repository import UserRepository
from src.infrastructure.utils.hash_service import HashService
from src.infrastructure.utils.token_service import TokenService
from src.infrastructure.utils.validate_email import is_valid_email


class UserService:
    @staticmethod
    async def create_user(user_data: UserRegistration) -> UserResponse:
        user_data = UserData(email=user_data.email, username=user_data.username, password_hash=HashService.hash(user_data.password))
        user = await UserRepository.create_user(user_data)

        user_dto = UserDto(id=str(user.id),
                           email=user.email,
                           username=user.username,
                           access_level=user.access_level,
                           is_email_verified=user.is_email_verified)

        access_token = AccessToken(access_token=await TokenService.create_access_token(user=user_dto))
        refresh_token = RefreshToken(refresh_token=await TokenService.create_refresh_token(user_id=user_dto.id))

        await UserRepository.add_refresh_token(user_id=user.id, refresh_token=refresh_token.refresh_token)

        return UserResponse(user=user_dto, access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    async def login(user_data: UserLogin) -> UserResponse:
        if is_valid_email(user_data.login):
            user = await UserRepository.get_user_by_email(user_data.login)
        else:
            user = await UserRepository.get_user_by_username(user_data.login)

        if not user:
            raise UserNotFoundException

        if not HashService.verify(user.password_hash, user_data.password):
            raise InvalidCredentialsException

        user_dto = UserDto(id=str(user.id),
                           email=user.email,
                           username=user.username,
                           access_level=user.access_level,
                           is_email_verified=user.is_email_verified)

        access_token = AccessToken(access_token=await TokenService.create_access_token(user=user_dto))
        refresh_token = RefreshToken(refresh_token=await TokenService.create_refresh_token(user_id=user_dto.id))

        await UserRepository.add_refresh_token(user_id=user.id, refresh_token=refresh_token.refresh_token)

        return UserResponse(user=user_dto, access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    async def verify_user(token: str) -> User:
        email = await TokenService.decode_verify_token(token)
        user = await UserRepository.get_user_by_email(email)
        if user is None:
            raise UserNotFoundByEmailException
        user.is_email_verified = True
        await UserRepository.update_user(user)
        return user

    @staticmethod
    async def create_tokens(refresh_token: str) -> UserResponse:
        token_data = await TokenService.decode_refresh_token(refresh_token)
        user_id = UUID(token_data["sub"])
        user = await UserRepository.get_user_by_id(user_id)

        if user is None:
            await UserRepository.delete_all_refresh_tokens(user_id=user_id)
            raise UserNotFoundException

        if refresh_token not in user.refresh_tokens:
            await UserRepository.delete_all_refresh_tokens(user_id=user_id)
            raise InvalidCredentialsException

        if len(user.refresh_tokens) > settings.MAX_REFRESH_TOKENS_IN_DB:
            await UserRepository.delete_all_refresh_tokens(user_id=user_id)
            raise TooManyRefreshTokensException

        user_dto = UserDto(id=str(user_id),
                           email=user.email,
                           username=user.username,
                           access_level=user.access_level,
                           is_email_verified=user.is_email_verified)

        refresh_token = RefreshToken(refresh_token=await TokenService.create_refresh_token(user_id=user_dto.id))
        access_token = AccessToken(access_token=await TokenService.create_access_token(user=user_dto))
        await UserRepository.add_refresh_token(user_id=user_id, refresh_token=refresh_token.refresh_token)

        return UserResponse(user=user_dto, access_token=access_token, refresh_token=refresh_token)
