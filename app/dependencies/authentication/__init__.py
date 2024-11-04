from typing import Annotated
from fastapi import Depends, Request, status
from fastapi_mctools.dependencies import Dependency
from fastapi_mctools.exceptions import HTTPException
from app.models.users import User
from app.dependencies.authentication.jwt import get_current_jwt_user
from app.dependencies.authentication.session import get_current_session_user


async def get_current_user(
    request: Request,
    session_user: Annotated[User, Depends(get_current_session_user)],
    jwt_user: Annotated[User, Depends(get_current_jwt_user)],
) -> User:
    if not session_user and not jwt_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증이 잘 못 되었거나 로그인이 되지 않았습니다.",
            code="UNAUTHORIZED",
        )

    if session_user:
        request.state.user = session_user
        return session_user
    if jwt_user:
        request.state.user = jwt_user
        return jwt_user


auth_dependency = Dependency(
    CurrentUser=get_current_user,
)
