import uuid
from datetime import datetime, timedelta, timezone

import jwt

from src.application.domain.user_domain import UserDto
from src.config import settings
from src.exceptions import TokenTimeIsExpiredException, InvalidTokenException


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
        refresh_token_id = uuid.uuid4()
        expire_delta = timedelta(minutes=settings.REFRESH_TTL_MINUTES)
        payload = {
            "sub": user_id,
            "jti": str(refresh_token_id),
            "exp": datetime.now(timezone.utc) + expire_delta,
        }
        token = jwt.encode(payload, settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)
        return token

    @staticmethod
    async def create_verify_token(email: str) -> str:
        expire_delta = timedelta(minutes=settings.CONFIRM_TTL_MINUTES)
        payload = {
            "sub": email,
            "exp": datetime.now(timezone.utc) + expire_delta
        }
        token = jwt.encode(payload, settings.CONFIRM_SECRET_KEY, algorithm=settings.ALGORITHM)
        return token

    @staticmethod
    async def decode_verify_token(token: str) -> str:
        try:
            payload = jwt.decode(token, settings.CONFIRM_SECRET_KEY, algorithms=[settings.ALGORITHM])
            expire_time = datetime.fromtimestamp(payload["exp"])
            if expire_time < datetime.now(timezone.utc):
                raise TokenTimeIsExpiredException
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise TokenTimeIsExpiredException
        except jwt.DecodeError:
            raise InvalidTokenException
