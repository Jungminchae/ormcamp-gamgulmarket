from fastapi import APIRouter, status
from fastapi_mctools.utils.responses import ResponseInterFace
from app.schemas import BaseResponse, ListResponse
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


@router.get("/rooms/{user_id}/", status_code=status.HTTP_200_OK)
async def get_chat_rooms(data: chat_dependency.GetChatRooms):
    """
    # 채팅방 목록 조회
    - **user_id**: 사용자 아이디
    """
    response = ResponseInterFace(result=data, message="유저 채팅방 목록 조회 완료")
    return ListResponse(**response)


@router.websocket("/ws/{room_id}/")
async def chat_endpoint(chat: chat_dependency.StartChat):
    """
    1:1 채팅하기
    """
