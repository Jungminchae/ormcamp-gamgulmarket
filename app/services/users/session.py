import secrets
from redis import asyncio as aioredis
from app.config.settings import settings


async def create_user_session(redis: aioredis.Redis, user_id: str) -> str:
    """
    유저 세션 생성

    * 세션 최대 개수 3개를 넘어가면 가장 오래된 세션을 삭제
    """
    session_key = secrets.token_hex(16)
    user_session_key = f"user:{user_id}"

    existing_session_key = await redis.smembers(user_session_key)
    if len(existing_session_key) > settings.MAX_SESSION_PER_USER:
        oldest_session_key = list(existing_session_key)[0]
        await redis.srem(user_session_key, oldest_session_key)
        await redis.delete(oldest_session_key)

    await redis.sadd(user_session_key, session_key)
    await redis.set(session_key, user_id, ex=settings.MAX_SESSION_AGE)

    return session_key
