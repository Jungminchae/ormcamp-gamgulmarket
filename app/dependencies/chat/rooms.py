from datetime import datetime
from app.schemas.chat.rooms import ChatRoomCreateRequest
from app.dependencies.core.redis import RedisMessageBroker
from app.dependencies.authentication import auth_dependency


async def create_chat_room(
    user: auth_dependency.CurrentUser,
    redis: RedisMessageBroker,
    data: ChatRoomCreateRequest,
) -> str:
    user_id = user.id
    target_user_id = data.target_user_id
    room_id = f"{user_id}:{target_user_id}" if user_id < target_user_id else f"{target_user_id}:{user_id}"
    result = {"room_id": room_id}

    if await redis.exists(room_id):
        return {"room_id": room_id}
    await redis.hset(room_id, mapping={"members": f"{user_id},{target_user_id}", "created_at": datetime.now().isoformat()})

    return result
