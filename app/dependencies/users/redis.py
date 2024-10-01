from redis import asyncio as aioredis
from app.config.settings import settings


async def get_session() -> aioredis.Redis:
    return aioredis.from_url(settings.SESSION_URL, decode_responses=True)
