from fastapi import APIRouter, status
from fastapi_mctools.utils.responses import ResponseInterFace
from app.schemas import BaseResponse
from app.dependencies.chat import chat_dependency


router = APIRouter()


@router.post("/rooms/", status_code=status.HTTP_201_CREATED)
async def create_chat_room(data: chat_dependency.CreateChatRoom):
    """
    # 채팅방 생성
    - **target_user_id**: 상대방 유저 아이디
    """
    response = ResponseInterFace(result=data, message="채팅방 생성 완료")
    return BaseResponse(**response)
