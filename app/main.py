from fastapi import FastAPI, Depends
from fastapi.security.api_key import APIKeyHeader
from app.routes.routers import router


def create_app():
    auth_header = APIKeyHeader(name="Authorization", auto_error=False)
    app = FastAPI(dependencies=[Depends(auth_header)])
    app.include_router(router)
    return app


app = create_app()
