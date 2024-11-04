from fastapi import Request
from app.db.async_session import DB
from app.orms.users import user_orm
from app.orms.products import product_orm
from app.services.core.permissions import PermissionChecker, IsMyself, IsOwner


async def check_user_permission(request: Request, db: DB):
    path_params = request.path_params
    user_id = path_params.get("user_id")
    obj = await user_orm.get_by_id(db, user_id)

    profile_permission = PermissionChecker(
        permissions=[IsMyself],
        obj=obj,
    )
    await profile_permission(request)


async def check_product_owner_permission(request: Request, db: DB):
    path_params = request.path_params
    product_id = path_params.get("product_id")
    product = await product_orm.get_by_id(db, product_id)

    product_permission = PermissionChecker(permissions=[IsOwner], obj=product)
    await product_permission(request)
