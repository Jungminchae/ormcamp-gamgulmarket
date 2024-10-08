from fastapi import APIRouter
from app.routes.endpoints import users as users_endpoints
from app.routes.endpoints import products as products_endpoints
from app.routes.endpoints import chat as chat_endpoints

router = APIRouter()


router.include_router(users_endpoints.router, prefix="/users", tags=["users"])
router.include_router(products_endpoints.router, prefix="/products", tags=["products"])
router.include_router(chat_endpoints.router, prefix="/chat", tags=["chat"])
