from fastapi import APIRouter, status
from fastapi_mctools.utils.responses import ResponseInterFace
from app.dependencies.users import users_dependency
from app.schemas import BaseResponse

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def register_user(data: users_dependency.RegisterUser):
    """
    # 유저 생성
    - **email**: 이메일
    - **password**: 비밀번호
    - **password_confirm**: 비밀번호 확인
    """
    response = ResponseInterFace(result=data, message="유저 생성 완료")
    return BaseResponse(**response)
