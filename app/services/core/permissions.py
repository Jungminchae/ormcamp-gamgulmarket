from typing import TYPE_CHECKING
from fastapi import status, Request
from fastapi_mctools.exceptions import HTTPException
from app.models.users import User

if TYPE_CHECKING:
    from app.models.users import User, Base


class BasePermission:
    def has_permission(self, request: Request) -> bool:
        return True

    def has_object_permission(self, request: Request, obj: "Base") -> bool:
        return True


class IsMyself(BasePermission):
    def has_object_permission(self, request: Request, obj: "User") -> bool:
        return obj.id == request.state.user.id


class IsOwner(BasePermission):
    def has_object_permission(self, request: Request, obj: "Base") -> bool:
        return obj.user_id == request.state.user.id


class PermissionChecker:
    def __init__(self, permissions: list[BasePermission], obj: "Base" = None):
        self.permissions = [permission() for permission in permissions]
        self.obj = obj
        self.permission_denied = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="권한이 없습니다.",
            code="FORBIDDEN",
        )

    def allow_superuser(self, request: Request) -> bool:
        try:
            if request.state.user.is_superuser:
                return True
        except AttributeError:
            return False

    def check_permissions(self, request: Request) -> bool:
        is_checked = all(permission.has_permission(request) for permission in self.permissions)
        if not is_checked:
            raise self.permission_denied

    def check_object_permissions(self, request: Request) -> bool:
        is_checked = all(permission.has_object_permission(request, self.obj) for permission in self.permissions)
        if not is_checked:
            raise self.permission_denied

    async def __call__(self, request: Request):
        if self.allow_superuser(request):
            return True

        self.check_permissions(request)
        if self.obj:
            self.check_object_permissions(request)
        return True
