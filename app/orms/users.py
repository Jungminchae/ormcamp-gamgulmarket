from sqlalchemy import select
from fastapi_mctools.orms.sqlalchemy import async_base
from app.models.users import User, Profile


class UserRead(async_base.AReadBase):
    async def get_user_profile(self, db, user_id):
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

    async def get_profile_obj(self, db, user_id):
        query = select(self.model2).where(self.model2.user_id == user_id)
        result = await db.execute(query)
        return self.get_result(result, [])


class UserCreate(async_base.ACreateBase): ...


class UserUpdate(async_base.AUpdateBase):
    async def update_profile(self, db, profile_input, profile_obj):
        profile_obj.profile = profile_obj.profile | profile_input
        await db.commit()
        await db.refresh(profile_obj)
        return profile_obj


class UserORM(UserRead, UserCreate, UserUpdate):
    def __init__(self, model, model2):
        self.model2 = model2
        super().__init__(model)


user_orm = UserORM(User, Profile)
