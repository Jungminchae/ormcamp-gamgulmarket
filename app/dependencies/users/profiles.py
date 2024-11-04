from fastapi.encoders import jsonable_encoder
from app.db.async_session import DB
from app.models.users import User
from app.schemas.users.profiles import ProfileUpdateRequest
from app.orms.users import user_orm
from app.dependencies.authentication import auth_dependency


async def get_user_profile(
    db: DB,
    user: auth_dependency.CurrentUser,
) -> User:
    user_id = user.id
    user_profile = await user_orm.get_user_profile(db, user_id)
    user_profile = jsonable_encoder(user_profile)
    return user_profile


async def update_user_profile(
    db: DB,
    user: auth_dependency.CurrentUser,
    data: ProfileUpdateRequest,
) -> User:
    profile_input = data.model_dump()
    profile_input = profile_input.get("profile")
    profile_obj = await user_orm.get_profile_obj(db, user.id)
    profile_obj = profile_obj["Profile"]
    updated_profile = await user_orm.update_profile(db, profile_input=profile_input, profile_obj=profile_obj)
    updated_profile = jsonable_encoder(updated_profile)
    return updated_profile
