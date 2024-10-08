from fastapi_mctools.dependencies import Dependency
from app.dependencies.chat.rooms import create_chat_room


chat_dependency = Dependency(
    CreateChatRoom=create_chat_room,
)
