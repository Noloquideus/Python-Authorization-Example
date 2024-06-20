from typing import Callable
from functools import wraps
from datetime import datetime, timezone
from src.exceptions import InvalidTokenException, TokenTimeIsExpiredException, InsufficientAccessLevelException
from src.infrastructure.utils.token_service import TokenService


def protect(min_access_level: int):
    def decorator(func: Callable):
        @wraps(func)
        async def decorated(*args, token: str, **kwargs):
            try:
                payload = await TokenService.decode_access_token(token)
            except Exception as e:
                raise InvalidTokenException

            access_level = payload.get("access_level", 0)
            exp = datetime.fromtimestamp(payload.get("exp"), timezone.utc)
            iat = datetime.fromtimestamp(payload.get("iat"), timezone.utc)

            if access_level < min_access_level:
                raise InsufficientAccessLevelException

            # Проверка времени жизни токена
            remaining_time = (exp - datetime.now(timezone.utc)).total_seconds()
            total_time = (exp - iat).total_seconds()

            if remaining_time <= 0:
                raise TokenTimeIsExpiredException

            if remaining_time <= 0.1 * total_time:
                new_token = await TokenService.create_access_token(payload)
                kwargs['new_token'] = new_token

            return await func(*args, **kwargs)
        return decorated
    return decorator
