from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis.asyncio as redis
from redis.asyncio.connection import ConnectionPool
from src.config import settings


async def init_redis():
    pool = ConnectionPool.from_url(url=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    r = redis.Redis(connection_pool=pool)
    FastAPICache.init(RedisBackend(r), prefix="cache")
