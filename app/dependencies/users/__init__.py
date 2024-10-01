from fastapi_mctools.dependencies import Dependency
from app.dependencies.users.registers import register_user_by_email
from app.dependencies.users.login import perform_session_login, perform_jwt_login

users_dependency = Dependency(
    RegisterUser=register_user_by_email,
    SessionLogin=perform_session_login,
    JWTLogin=perform_jwt_login,
)
