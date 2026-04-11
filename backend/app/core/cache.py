import json
import os
from functools import wraps
import redis.asyncio as redis
from fastapi import Request, Response
from app.core.config import settings

redis_url = getattr(settings, "REDIS_URL", os.getenv("REDIS_URL", "redis://localhost:6379/0"))

redis_client = redis.from_url(
    redis_url,
    encoding="utf-8", 
    decode_responses=True
)

async def init_cache():
    pass

async def close_cache():
    await redis_client.close()

async def get_redis():
    yield redis_client

async def clear_cache(pattern="*"):
    keys = await redis_client.keys(pattern)
    if keys:
        await redis_client.delete(*keys)
    return len(keys)

def cache(expire=3600):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get("request")
            response = kwargs.get("response")
            
            if not request:
                return await func(*args, **kwargs)
            
            cache_key = f"api_cache:{request.url.path}"
            
            cached_data = await redis_client.get(cache_key)
            if cached_data:
                if response:
                    response.headers["X-Cache"] = "HIT"
                return json.loads(cached_data)
            
            result = await func(*args, **kwargs)
            
            await redis_client.set(cache_key, json.dumps(result), ex=expire)
            if response:
                response.headers["X-Cache"] = "MISS"
                
            return result
        return wrapper
    return decorator


async def check_rate_limit(key: str, max_requests: int = 5, window: int = 60):
    """Check rate limit via Redis. Raises HTTPException(429) if exceeded.
    Silently skips if Redis is unavailable — never blocks legitimate requests."""
    from fastapi import HTTPException
    try:
        current = await redis_client.get(key)
        if current and int(current) >= max_requests:
            raise HTTPException(
                status_code=429,
                detail="Too many requests, please try again later",
            )
        pipe = redis_client.pipeline()
        pipe.incr(key)
        pipe.expire(key, window)
        await pipe.execute()
    except HTTPException:
        raise
    except Exception:
        pass

