from src.config import settings
from src.infrastructure.database.database import async_session_maker
from src.infrastructure.database.models import User
from src.infrastructure.utils.hash_service import HashService


async def create_superadmin():
    async with async_session_maker() as session:
        superadmin = User(
            email=settings.SUPERADMIN_EMAIL,
            username=settings.SUPERADMIN_USERNAME,
            password_hash=HashService.hash(settings.SUPERADMIN_PASSWORD),
            access_level=settings.SUPERADMIN_ACCESS_LEVEL)
        session.add(superadmin)
        await session.commit()
