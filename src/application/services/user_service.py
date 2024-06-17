from src.application.domain.user_domain import UserRegistration, UserData
from src.infrastructure.database.repositories.user_repository import UserRepository
from src.infrastructure.utils.hash_service import HashService


class UserService:

    @staticmethod
    async def create_user(user_data: UserRegistration):
        user_data = UserData(email=user_data.email, username=user_data.username, password_hash=HashService.hash(user_data.password))
        user = await UserRepository.create_user(user_data)
        return user
