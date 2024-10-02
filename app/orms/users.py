from sqlalchemy import select
from fastapi_mctools.orms.sqlalchemy import async_base
from app.models.users import User, Profile


class UserRead(async_base.AReadBase):
    async def get_user_profile(self, db, user_id):
        self.model2
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
                self.model2.id.label("profile_id"),
                self.model2.profile,
            )
            .where(self.model.id == user_id)
            .join(self.model.profiles)
        )
        result = await db.execute(query)
        return self.get_result(result, [])


class UserCreate(async_base.ACreateBase): ...


class UserORM(UserRead, UserCreate):
    def __init__(self, model, model2):
        self.model2 = model2
        super().__init__(model)


user_orm = UserORM(User, Profile)
