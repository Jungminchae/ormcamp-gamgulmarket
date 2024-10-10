from redis import asyncio as aioredis


class ChatMessageService:
    def __init__(
        self,
        redis: aioredis.Redis,
        user_profile: dict,
        target_user_profile: dict,
        room_id: int,
    ) -> None:
        self.redis = redis
        self.user = user_profile
        self.target_user = target_user_profile
        self.room_id = room_id

    async def init_chat_room(self, chat_room_data: dict) -> None:
        await self.redis.hset(f"room:{self.room_id}", mapping=chat_room_data)

    async def add_users_to_list(self):
        await self.redis.sadd(f"user:{self.user["user_id"]}:rooms", self.room_id)
        await self.redis.sadd(f"user:{self.target_user['user_id']}:rooms", self.room_id)

    async def add_users_basic_info(self) -> None:
        if not await self.redis.hexists(f"user:{self.user["user_id"]}:info", "name"):
            await self.redis.hset(
                f"user:{self.user["user_id"]}:info",
                mapping={"name": f"{self.user["profile"]["name"]}"},
            )
        if not await self.redis.hexists(f"user:{self.target_user["user_id"]}:info", "name"):
            await self.redis.hset(
                f"user:{self.target_user["user_id"]}:info",
                mapping={"name": f"{self.target_user["profile"]["name"]}"},
            )
