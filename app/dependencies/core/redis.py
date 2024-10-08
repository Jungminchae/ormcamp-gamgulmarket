from typing import Annotated
from fastapi import Depends
from redis import asyncio as aioredis
from app.config.settings import settings


async def get_session() -> aioredis.Redis:
    return aioredis.from_url(settings.SESSION_URL, decode_responses=True)


async def get_message_broker() -> aioredis.Redis:
    return aioredis.from_url(settings.MESSAGE_BROKER_URL, decode_responses=True)


RedisSession = Annotated[aioredis.Redis, Depends(get_session)]
RedisMessageBroker = Annotated[aioredis.Redis, Depends(get_message_broker)]
