from sqlalchemy import UUID
from sqlalchemy.exc import IntegrityError
from src.application.domain.user_domain import UserData
from src.exceptions import UserAlreadyExistsException
from src.infrastructure.database.database import async_session_maker
from src.infrastructure.database.models import User


class UserRepository:
    @staticmethod
    async def create_user(user_data: UserData) -> User:
        async with async_session_maker() as session:
            try:
                user_model = User(email=user_data.email, username=user_data.username, password_hash=user_data.password_hash)
                session.add(user_model)
                await session.commit()
                return user_model
            except IntegrityError:
                await session.rollback()
                raise UserAlreadyExistsException

    @staticmethod
    async def add_refresh_token(user_id: UUID, refresh_token: str) -> None:
        async with async_session_maker() as session:
            user = await session.get(User, user_id)
            if user.refresh_tokens is None:
                user.refresh_tokens = []
            user.refresh_tokens.append(refresh_token)
            await session.commit()
