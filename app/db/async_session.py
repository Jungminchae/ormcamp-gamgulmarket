from fastapi_mctools.db.sqlalchemy import AsyncDB
from app.config.settings import settings


get_db = AsyncDB(
    settings.DB_URL, autoflush=False, autocommit=False, expire_on_commit=False
)
