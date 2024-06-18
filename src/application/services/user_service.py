from src.application.domain.jwt import RefreshToken, AccessToken
from src.application.domain.user_domain import UserRegistration, UserData, UserDto, UserResponse
from src.infrastructure.database.repositories.user_repository import UserRepository
from src.infrastructure.utils.hash_service import HashService
from src.infrastructure.utils.token_service import TokenService


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

        return UserResponse(user=user_dto, access_token=access_token, refresh_token=refresh_token)
