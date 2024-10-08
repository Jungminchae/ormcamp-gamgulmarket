from pydantic import BaseModel


class ChatRoomCreateRequest(BaseModel):
    target_user_id: int
