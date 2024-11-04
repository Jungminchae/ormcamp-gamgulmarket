import asyncio
from typing import NoReturn
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect
from app.db.async_session import DB
from app.schemas.chat.rooms import ChatRoomCreateRequest
from app.orms.users import user_orm
from app.dependencies.core.redis import RedisMessageBroker
from app.dependencies.authentication import auth_dependency
from app.services.chat.messages import ChatMessageService
from app.services.chat.connections import ConnectionService


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

    if await redis.hexists(f"room:{room_id}", "members"):
        return result

    await chat_message.init_chat_room(chat_room_data)
    await chat_message.add_users_to_list()
    await chat_message.add_users_basic_info()

    return result


async def get_chat_rooms(
    user: auth_dependency.CurrentUser,
    redis: RedisMessageBroker,
    user_id: int,
) -> list[dict]:
    chat_message = ChatMessageService(redis)
    chat_rooms = await chat_message.scan_chat_rooms(user_id)

    if not chat_rooms:
        return []
    chat_rooms_info = await chat_message.get_chat_rooms_info(chat_rooms, user_id)
    return chat_rooms_info


async def start_chat(
    websocket: WebSocket,
    user: auth_dependency.CurrentUser,
    redis: RedisMessageBroker,
    room_id: str,
) -> NoReturn:
    user_id = user.id
    conection = ConnectionService(redis)
    conection.validate_connection(room_id, user_id)

    await conection.connect(room_id, user_id, websocket)
    pubsub_task = asyncio.create_task(conection.handle_pub_sub(room_id))

    try:
        while True:
            data = await websocket.receive_text()
            await conection.send_message(room_id, data)
    except WebSocketDisconnect:
        await conection.disconnect(room_id, user_id)
        pubsub_task.cancel()
