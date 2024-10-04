from fastapi_mctools.dependencies import Dependency
from app.dependencies.permissions.authenticated import is_user_myself


permission_dependency = Dependency(
    IsUserMyself=is_user_myself,
)
