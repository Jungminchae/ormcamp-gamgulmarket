from typing import Annotated
from fastapi import Depends, Form, status
from fastapi_mctools.exceptions import HTTPException

from app.db.async_session import DB
from app.schemas.users.registers import RegisterUserRequest
from app.orms.users import user_orm
from app.services.users.password import PasswordService


async def check_email_exists(data: Annotated[RegisterUserRequest, Form()], db: DB) -> RegisterUserRequest:
    user = await user_orm.get_by_filters(db, columns=["email"], email=data.email)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 이메일입니다.", code="EMAIL_EXISTS")
    return data


async def register_user_by_email(vaild_data: Annotated[RegisterUserRequest, Depends(check_email_exists)], db: DB) -> dict:
    data = vaild_data.model_dump()
    password = PasswordService.get_password_hash(data.get("password"))
    data = {
        "email": data.get("email"),
        "password": password,
    }

    user = await user_orm.create(db, **data)
    result = {
        "id": user.id,
        "email": user.email,
    }
    return result
