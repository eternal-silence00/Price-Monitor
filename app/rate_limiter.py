from fastapi import HTTPException, Request
from app.redis_client import redis_client

async def rate_limit(request: Request):
    key = f"rate_limit:{request.client.host}:{request.url.path}"
    attemps = await redis_client.get(key)
    if attemps and int(attemps) >= 5:
        raise HTTPException(status_code=429, detail="Too many requests")
    await redis_client.incr(key)
    await redis_client.expire(key, 60)