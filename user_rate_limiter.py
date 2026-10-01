import asyncio
from Redis_client import get_redis
from fastapi import Depends,HTTPException, Request



async def user_rate_limiter(request:Request, redis_client=Depends(get_redis)):
    user_id= request.path_params.get("user_id",1)
    key = f"rate:user:{user_id}"
    script = """
        local count = redis.call('INCR', KEYS[1])
        if count == 1 then
            redis.call('EXPIRE', KEYS[1], ARGV[1])
        end
        return count
    
    """
    
    rate_limiter_script = redis_client.register_script(script)
    count= await rate_limiter_script(key,60)
    if count > 5:
        raise HTTPException(
            status_code = 429,
            detail = "Too many requests"
        )
    