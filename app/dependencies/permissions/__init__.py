from fastapi_mctools.dependencies import Dependency
from app.dependencies.permissions.authenticated import is_user_myself, is_product_owner


permission_dependency = Dependency(
    IsUserMyself=is_user_myself,
    IsProductOwner=is_product_owner,
)
