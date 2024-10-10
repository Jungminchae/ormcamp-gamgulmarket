from typing import Annotated
from fastapi import Depends, Request
from app.db.async_session import DB
from app.dependencies.core.redis import RedisSession
from app.orms.users import user_orm


async def validate_session(request: Request, redis: RedisSession) -> str | None:
    cookie_session = request.cookies.get("session")
    authorization_session = request.headers.get("Authorization")
    if not cookie_session and not authorization_session:
        return None

    if authorization_session.startswith("Bearer"):
        return None

    if cookie_session:
        user_id = await redis.get(cookie_session)

    elif authorization_session:
        user_id = await redis.get(authorization_session)
    return int(user_id)


async def get_current_session_user(user_id: Annotated[int, Depends(validate_session)], db: DB) -> dict:
    if not user_id:
        return None
    user = await user_orm.get_by_filters(db, id=user_id)
    if not user:
        return None
    return user[0]
