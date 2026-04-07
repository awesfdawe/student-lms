import json
import functools
import hashlib
from redis.asyncio import Redis, ConnectionPool
from app.core.config import settings

_pool = None
_redis = None


async def init_cache():
    global _pool, _redis
    _pool = ConnectionPool.from_url(
        settings.valkey_url,
        decode_responses=True,
        max_connections=20,
    )
    _redis = Redis(connection_pool=_pool)
    await _redis.ping()


async def close_cache():
    global _redis, _pool
    if _redis:
        await _redis.aclose()
    if _pool:
        await _pool.aclose()


def get_redis():
    return _redis


async def clear_cache(collection_name):
    r = get_redis()
    if not r:
        return 0
    pattern = f"cache:{collection_name}:*"
    deleted = 0
    async for key in r.scan_iter(match=pattern, count=200):
        await r.delete(key)
        deleted += 1
    return deleted


async def clear_all_cache():
    r = get_redis()
    if not r:
        return 0
    deleted = 0
    async for key in r.scan_iter(match="cache:*", count=200):
        await r.delete(key)
        deleted += 1
    return deleted


def _build_cache_key(prefix, request):
    raw = f"{request.url.path}?{request.url.query}"
    h = hashlib.md5(raw.encode()).hexdigest()
    return f"cache:{prefix}:{h}"


def cache(prefix, ttl=300):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            from fastapi import Request
            request = kwargs.get("request")
            if not request:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break

            r = get_redis()
            if not r or not request:
                return await func(*args, **kwargs)

            key = _build_cache_key(prefix, request)

            cached = await r.get(key)
            if cached is not None:
                return json.loads(cached)

            result = await func(*args, **kwargs)
            await r.set(key, json.dumps(result, default=str), ex=ttl)
            return result

        return wrapper
    return decorator
