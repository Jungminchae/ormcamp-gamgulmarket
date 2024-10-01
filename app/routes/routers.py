from fastapi import APIRouter
from app.routes.endpoints import users as users_endpoints

router = APIRouter()


router.include_router(users_endpoints.router, prefix="/users", tags=["users"])
