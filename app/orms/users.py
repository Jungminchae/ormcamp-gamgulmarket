from fastapi_mctools.orms.sqlalchemy import async_base
from app.models.users import User


class UserRead(async_base.AReadBase): ...


class UserCreate(async_base.ACreateBase): ...


class UserORM(UserRead, UserCreate):
    def __init__(self, model):
        super().__init__(model)


user_orm = UserORM(User)
