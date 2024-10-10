from datetime import datetime
from app.db.async_session import DB
from app.schemas.chat.rooms import ChatRoomCreateRequest
from app.orms.users import user_orm
from app.dependencies.core.redis import RedisMessageBroker
from app.dependencies.authentication import auth_dependency
from app.dependencies.permissions import permission_dependency
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

    if await redis.hexists(f"room:{room_id}", "members"):
        return result

    await chat_message.init_chat_room(chat_room_data)
    await chat_message.add_users_to_list()
    await chat_message.add_users_basic_info()

    return result


async def get_chat_rooms(
    user: permission_dependency.IsUserMyself,
    redis: RedisMessageBroker,
    user_id: int,
) -> list[dict]:
    chat_message = ChatMessageService(redis)
    chat_rooms = await chat_message.scan_chat_rooms(user_id)

    if not chat_rooms:
        return []
    chat_rooms_info = await chat_message.get_chat_rooms_info(chat_rooms, user_id)
    return chat_rooms_info


# from typing import List, Dict
# from fastapi import FastAPI, Depends, HTTPException
# from aioredis import Redis

# app = FastAPI()

# # Redis 클라이언트 객체 생성 (필요에 따라 설정)
# redis_broker = RedisMessageBroker()


# async def get_user_chat_rooms(user_id: str, redis: Redis) -> List[Dict[str, str]]:
#     """
#     특정 사용자가 참여 중인 모든 채팅방 목록과 대화 상대, 마지막 메시지를 조회하는 함수.
#     """
#     # 1. 사용자가 참여 중인 모든 채팅방 ID 조회
#     chat_rooms = await redis.smembers(f"user:{user_id}:rooms")
#     if not chat_rooms:
#         return []

#     chat_data = []

#     for room_id in chat_rooms:
#         # 2. 채팅방의 멤버 정보 가져오기
#         members = await redis.hget(room_id, "members")
#         if not members:
#             continue

#         # 3. 채팅방 멤버에서 현재 사용자를 제외한 대화 상대 ID 추출
#         other_user_id = [uid for uid in members.split(",") if uid != user_id]
#         if not other_user_id:
#             continue
#         other_user_id = other_user_id[0]  # 대화 상대 ID가 한 명이므로 첫 번째 항목 선택

#         # 4. 대화 상대방의 이름 조회 (user:{user_id}:info 해시에서 name 필드 가져오기)
#         other_user_name = await redis.hget(f"user:{other_user_id}:info", "name")
#         if not other_user_name:
#             continue

#         # 5. 채팅방의 마지막 메시지 조회
#         last_message = await redis.hget(f"room:{room_id}", "last_message")
#         if not last_message:
#             last_message = "대화 내용이 없습니다."  # 기본 메시지

#         # 6. 조회된 데이터를 리스트에 추가
#         chat_data.append({
#             "user_name": other_user_name,
#             "last_message": last_message
#         })

#     return chat_data


# @app.get("/user/{user_id}/chat-rooms/")
# async def user_chat_rooms(user_id: str, redis: Redis = Depends(lambda: redis_broker.redis)):
#     """
#     사용자가 참여 중인 모든 채팅방 목록과 마지막 메시지, 상대방 이름을 반환하는 엔드포인트.
#     """
#     chat_data = await get_user_chat_rooms(user_id, redis)
#     if not chat_data:
#         raise HTTPException(status_code=404, detail="No chat rooms found for the user.")
#     return {"user_id": user_id, "chat_rooms": chat_data}

# async def send_message(room_id: str, user_id: str, message: str, redis: Redis):
#     """
#     채팅방에 메시지를 전송하고, 마지막 메시지를 업데이트하는 함수.
#     """
#     # 메시지를 채팅방에 발행 (예: Pub/Sub 사용 가능)
#     await redis.publish(room_id, f"{user_id}: {message}")

#     # 채팅방의 마지막 메시지 업데이트
#     await redis.hset(
#         f"room:{room_id}",
#         mapping={"last_message": message, "timestamp": datetime.now().isoformat()}
#     )
