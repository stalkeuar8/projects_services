import redis.asyncio as redis
from app.settings.config import redis_settings
from typing import AsyncGenerator

redis_client = redis.from_url(redis_settings.REDIS_url, decode_responses=True)


async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    try:
        yield redis_client
        
    finally:
        pass