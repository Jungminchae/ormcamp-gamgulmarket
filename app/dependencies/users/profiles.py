from fastapi.encoders import jsonable_encoder
from app.db.async_session import DB
from app.models.users import User
from app.orms.users import user_orm
from app.dependencies.authentication import auth_dependency


async def get_user_profile(db: DB, user: auth_dependency.CurrentUser) -> User:
    user_id = user.id
    user_profile = await user_orm.get_user_profile(db, user_id)
    user_profile = jsonable_encoder(user_profile)
    return user_profile
