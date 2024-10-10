from fastapi_mctools.dependencies import Dependency
from app.dependencies.chat.rooms import create_chat_room, get_chat_rooms


chat_dependency = Dependency(
    CreateChatRoom=create_chat_room,
    GetChatRooms=get_chat_rooms,
)
