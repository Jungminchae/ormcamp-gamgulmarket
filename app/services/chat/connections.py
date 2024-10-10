import asyncio
from fastapi import WebSocket, WebSocketDisconnect, status
from redis import asyncio as aioredis


class ConnectionService:
    def __init__(self, redis: aioredis.Redis):
        self.redis = redis

    def validate_connection(self, room_id: str, user_id: str):
        chat_users = room_id.split(":")
        if str(user_id) not in chat_users:
            raise WebSocketDisconnect(code=status.WS_1008_POLICY_VIOLATION, reason="채팅방에 참여할 수 없습니다.")

    async def connect(self, room_id: str, user_id: str, websocket: WebSocket):
        await websocket.accept()
        await self.redis.sadd(f"connections:{room_id}", user_id)
        await self.redis.hset(f"user_room:{user_id}", "room_id", room_id)

    async def disconnect(self, room_id: str, user_id: str):
        await self.redis.srem(f"connections:{room_id}", user_id)
        await self.redis.hdel(f"user_room:{user_id}", "room_id")

    async def send_message(self, room_id: str, message: str):
        chat_users = room_id.split(":")
        for _ in chat_users:
            await self.redis.publish(f"room:{room_id}", message)
        await self.redis.hset(f"room:{room_id}", "last_message", message)

    async def handle_pub_sub(self, room_id: str):
        channel = f"room:{room_id}"
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(channel)

        try:
            while True:
                message = await pubsub.get_message(True)
                if message and message["type"] == "message":
                    data = message["data"]
                    await self.send_message(room_id, data)
        except asyncio.CancelledError:
            await pubsub.unsubscribe(channel)
            await pubsub.close()
