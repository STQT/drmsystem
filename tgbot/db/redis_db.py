import aioredis


async def get_redis():
    # Create a Redis connection
    redis = await aioredis.create_redis_pool('redis://redis:6380/0')
    return redis
