from typing import Annotated
from fastapi import Depends, Form, status
from fastapi_mctools.exceptions import HTTPException
from app.db.async_session import DB
from app.schemas.users.login import LoginRequest
from app.orms.users import user_orm
from app.models.users import User
from app.services.users.password import PasswordService
from app.services.users.session import create_user_session
from app.services.users.jwt import jwt_service
from app.dependencies.core.redis import RedisSession


async def validate_user(data: Annotated[LoginRequest, Form()], db: DB) -> User:
    email = data.email
    password = data.password

    user = await user_orm.get_by_filters(db, email=email)
    if not user or not PasswordService.verify_password(password, user[0].password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="유효하지 않은 아이디 또는 비밀번호", code="INVALID_CREDENTIALS"
        )
    return user[0]


async def perform_session_login(vaild_user: Annotated[User, Depends(validate_user)], redis: RedisSession) -> str:
    """
    # 쿠키에 세션 키 저장
    response.set_cookie(
        key=session,
        value=sesseion_key,
        httponly=True,  -> HttpOnly 속성으로 자바스크립트 접근 차단
        max_age=settings.MAX_SESSION_AGE,
        secure=True,  # HTTPS 연결에서만 전송
        samesite="", -> [Strict, Lax, None] 설정
    )
    """

    sesseion_key = await create_user_session(redis, vaild_user.id)
    return {"key": sesseion_key}


async def perform_jwt_login(vaild_user: Annotated[User, Depends(validate_user)]) -> str:
    data = {"id": str(vaild_user.id)}
    access_token = jwt_service.create_access_token(data)
    refresh_token = jwt_service.create_refresh_token(data)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
