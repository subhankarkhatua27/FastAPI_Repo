from redis.asyncio import Redis
from fastapi import Request


async def get_redis(request:Request):
    return request.app.state.redis