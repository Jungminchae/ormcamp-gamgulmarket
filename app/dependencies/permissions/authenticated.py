from typing import TYPE_CHECKING
from fastapi import status
from fastapi_mctools.exceptions import HTTPException
from app.db.async_session import DB
from app.orms.users import user_orm
from app.orms.products import product_orm
from app.dependencies.authentication import auth_dependency

if TYPE_CHECKING:
    from app.models.users import User


async def is_user_myself(db: DB, user: auth_dependency.CurrentUser, user_id: int) -> "User":
    if (user is None) or (user.id != user_id and not user.is_superuser):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="권한이 없습니다.",
            code="FORBIDDEN",
        )
    allowed_user = await user_orm.get_by_id(db, user_id)
    return allowed_user


async def is_product_owner(db: DB, user: auth_dependency.CurrentUser, product_id: int) -> "User":
    product = await product_orm.get_by_id(db, product_id)
    if (user is None) or (product.user_id != user.id and not user.is_superuser):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="권한이 없습니다.",
            code="FORBIDDEN",
        )
    return product
