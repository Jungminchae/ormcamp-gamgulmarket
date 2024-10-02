from sqlalchemy import select
from fastapi_mctools.orms.sqlalchemy import async_base
from app.models.users import User, Profile


class UserRead(async_base.AReadBase):
    async def get_user_profile(self, db, user_id):
        profile_model = Profile
        query = (
            select(
                self.model.id.label("user_id"),
                self.model.email,
                self.model.created_at,
                self.model.updated_at,
                self.model.deleted_at,
                self.model.is_active,
                self.model.is_superuser,
                self.model.is_removable,
                profile_model.id.label("profile_id"),
                profile_model.profile,
            )
            .where(self.model.id == user_id)
            .join(self.model.profiles)
        )
        result = await db.execute(query)
        return self.get_result(result, [])


class UserCreate(async_base.ACreateBase): ...


class UserORM(UserRead, UserCreate):
    def __init__(self, model):
        super().__init__(model)


user_orm = UserORM(User)
