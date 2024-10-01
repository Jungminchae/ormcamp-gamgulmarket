from fastapi_mctools.dependencies import Dependency
from app.dependencies.users.registers import register_user_by_email

users_dependency = Dependency(RegisterUser=register_user_by_email)
