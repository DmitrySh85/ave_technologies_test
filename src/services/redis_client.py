from redis.asyncio import Redis
from settings import settings


redis_client = Redis.from_url(settings.redis_url, decode_responses=False)

async def get_redis() -> Redis:
    return redis_client