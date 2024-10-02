from typing import Annotated
from fastapi import Depends, HTTPException, Request, status
from fastapi.security.utils import get_authorization_scheme_param
from app.db.async_session import DB
from app.orms.users import user_orm
from app.services.users.jwt import jwt_service


async def validate_token(request: Request) -> str | None:
    authorization = request.headers.get("Authorization")
    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        return None
    return param


class JWTAuthentication:
    async def __call__(
        self,
        db: DB,
        token: Annotated[str | None, Depends(validate_token)],
    ):
        if not token:
            return None

        try:
            valid_payload = jwt_service.check_token_expired(token)
            if valid_payload:
                id = valid_payload.get("id")
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Expired or changed token.",
                    headers={"WWW-Authenticate": "Bearer"},
                    code="EXPIRED_TOKEN",
                )
        except HTTPException as e:
            raise e
        else:
            user = await user_orm.get_by_id(db, id)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Non-existent user",
                    headers={"WWW-Authenticate": "Bearer"},
                    code="INVALID_USER",
                )
            else:
                return user


get_current_jwt_user = JWTAuthentication()
