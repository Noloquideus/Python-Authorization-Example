from datetime import datetime, timedelta, timezone
from src.application.domain.user_domain import UserDto
from src.config import settings


class TokenService:
    @staticmethod
    async def create_access_token(user: UserDto) -> str:
        expire_delta = timedelta(minutes=settings.ACCESS_TTL_MINUTES)
        payload = {
            "sub": user.id,
            "email": user.email,
            "username": user.username,
            "access_level": user.access_level,
            "is_email_verified": user.is_email_verified,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + expire_delta
        }
        token = jwt.encode(payload, settings.ACCESS_SECRET_KEY, algorithm=settings.ALGORITHM)
        return token

    @staticmethod
    async def create_refresh_token(user_id: str) -> str:
        pass
