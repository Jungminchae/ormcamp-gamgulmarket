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


@router.post("/login/session/", status_code=status.HTTP_200_OK)
async def login_session(data: users_dependency.SessionLogin):
    """
    # 세션 로그인
    - **email**: 이메일
    - **password**: 비밀번호
    """
    response = ResponseInterFace(result=data, message="로그인 성공")
    return BaseResponse(**response)


@router.post("/login/jwt/", status_code=status.HTTP_200_OK)
async def login_jwt(data: users_dependency.JWTLogin):
    """
    # JWT 로그인
    - **email**: 이메일
    - **password**: 비밀번호
    """
    response = ResponseInterFace(result=data, message="로그인 성공")
    return BaseResponse(**response)
