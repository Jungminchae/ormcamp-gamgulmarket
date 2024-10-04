from typing import TYPE_CHECKING
from fastapi import status
from fastapi_mctools.exceptions import HTTPException
from app.dependencies.authentication import auth_dependency

if TYPE_CHECKING:
    from app.models.users import User


async def is_user_myself(user: auth_dependency.CurrentUser, user_id: int) -> "User":
    if user.id != user_id and not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="권한이 없습니다.",
            code="FORBIDDEN",
        )

    return user
