from datetime import datetime
from app.db.async_session import DB
from app.schemas.chat.rooms import ChatRoomCreateRequest
from app.orms.users import user_orm
from app.dependencies.core.redis import RedisMessageBroker
from app.dependencies.authentication import auth_dependency
from app.services.chat.messages import ChatMessageService


async def create_chat_room(
    db: DB,
    user: auth_dependency.CurrentUser,
    redis: RedisMessageBroker,
    data: ChatRoomCreateRequest,
) -> str:
    user_id = user.id
    target_user_id = data.target_user_id
    user = await user_orm.get_user_profile(db, user_id)
    target_user = await user_orm.get_user_profile(db, target_user_id)
    room_id = f"{user_id}:{target_user_id}" if user_id < target_user_id else f"{target_user_id}:{user_id}"
    current_timestamp = datetime.now().isoformat()
    result = {"room_id": room_id}
    chat_room_data = {"members": f"{user_id},{target_user_id}", "last_message": "", "timestamp": current_timestamp}
    chat_message = ChatMessageService(redis, user, target_user, room_id)

    if await redis.hexists(room_id, "members"):
        return result

    await chat_message.init_chat_room(chat_room_data)
    await chat_message.add_users_to_list()

    return result
