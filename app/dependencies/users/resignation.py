from typing import TYPE_CHECKING, NoReturn
from fastapi import status
from fastapi_mctools.exceptions import HTTPException
from app.db.async_session import DB
from app.schemas.users.resignation import ResignationRequest
from app.orms.users import user_orm
from app.dependencies.permissions import permission_dependency
from app.services.users.password import PasswordService

if TYPE_CHECKING:
    pass


async def resign_user(
    db: DB,
    user: permission_dependency.IsUserMyself,
    data: ResignationRequest,
) -> NoReturn:
    """
    PostgreSQL 레벨에서 소프트 딜리트를 수행함
    - is_active = False, deleted_at = now() 가 추가됨
    """
    if not PasswordService.verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="비밀번호가 일치하지 않습니다.", code="INVALID_PASSWORD"
        )
    resignation_reason = data.resignation_reason
    user_id = user.id
    await user_orm.delete_user(db, user.id)
    await user_orm.update_by_filters(db, (user_orm.model.id == user_id,), **{"resignation_reason": resignation_reason})

    return
