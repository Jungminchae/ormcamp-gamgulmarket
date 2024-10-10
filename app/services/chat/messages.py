from redis import asyncio as aioredis


class ChatMessageService:
    def __init__(
        self,
        redis: aioredis.Redis,
        user_profile: dict | None = None,
        target_user_profile: dict | None = None,
        room_id: int | None = None,
    ) -> None:
        self.redis = redis
        self.user = user_profile
        self.target_user = target_user_profile
        self.room_id = room_id

    async def init_chat_room(self, chat_room_data: dict) -> None:
        """
        처음 채팅을 시작하는 경우 초기 세팅을 해야함
        """
        await self.redis.hset(f"room:{self.room_id}", mapping=chat_room_data)

    async def add_users_to_list(self):
        """
        채팅 목록에 사용자를 추가해서 특정 사용자가 참여 중인 채팅방 목록을 조회할 수 있도록 함
        """
        await self.redis.sadd(f"user:{self.user["user_id"]}:rooms", self.room_id)
        await self.redis.sadd(f"user:{self.target_user['user_id']}:rooms", self.room_id)

    async def add_users_basic_info(self) -> None:
        """
        채팅 사용자의 기본 정보를 추가함
        - 사용자 닉네임만 추가
        """
        if not await self.redis.hexists(f"user:{self.user["user_id"]}:info", "nickname"):
            await self.redis.hset(
                f"user:{self.user["user_id"]}:info",
                mapping={
                    "user_id": f"{self.user["user_id"]}",
                    "nickname": f"{self.user["profile"]["nickname"]}",
                },
            )
        if not await self.redis.hexists(f"user:{self.target_user["user_id"]}:info", "nickname"):
            await self.redis.hset(
                f"user:{self.target_user["user_id"]}:info",
                mapping={
                    "user_id": f"{self.target_user["user_id"]}",
                    "nickname": f"{self.target_user["profile"]["nickname"]}",
                },
            )

    async def scan_chat_rooms(self, user_id: int) -> list:
        """
        사용자가 참여 중인 모든 채팅방 목록을 조회함
        """
        chat_rooms = await self.redis.smembers(f"user:{user_id}:rooms")
        return chat_rooms

    async def get_chat_rooms_info(self, chat_rooms: list, user_id: int) -> dict:
        """
        채팅방 정보를 조회함
        - 멤버 정보 가져오기
        - 멤버 정보에서 대화 상대 ID 추출
        - 대화 상대방의 이름 조회
        - 채팅방의 마지막 메시지 조회
        """
        chat_rooms_info = []
        for room_id in chat_rooms:
            members = await self.redis.hget(f"room:{room_id}", "members")
            if not members:
                continue
            target_user_id = [target_user_id for target_user_id in members.split(",") if int(target_user_id) != user_id]
            if not target_user_id:
                continue

            target_user_id = target_user_id[0]

            target_user_profile = await self.redis.hmget(f"user:{target_user_id}:info", "user_id", "nickname")

            if not target_user_profile:
                continue
            last_message = await self.redis.hget(f"room:{room_id}", "last_message")

            chat_rooms_info.append(
                {
                    "user_id": target_user_profile[0],
                    "nickname": target_user_profile[1],
                    "last_message": last_message,
                }
            )
        return chat_rooms_info
