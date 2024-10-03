from pathlib import Path
from zoneinfo import ZoneInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DEBUG: bool = True
    OPENAPI_URL: str | None = "/openapi.json" if DEBUG else None
    API_PREFIX: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    TEST_DB_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/test"
    SESSION_URL: str = "redis://localhost:6379/0"
    TIMEZONE_LOCATION: str = "Asia/Seoul"
    ALLOWED_HOSTS: list = []
    CORS_ORIGINS: list = []

    MAX_SESSION_PER_USER: int = 3
    MAX_SESSION_AGE: int = 60 * 60 * 24 * 7

    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = "secret"
    JWT_ACCESS_TOKEN_EXPIRE_TIME: int = 60
    JWT_REFRESH_TOKEN_EXPIRE_TIME: int = 60 * 60 * 24 * 7

    SWAGGER_UI_PARAMS: dict = {
        "deepLinking": True,
        "defaultModelsExpandDepth": 1,
        "defaultModelExpandDepth": 1,
        "defaultModelRendering": "example",
        "displayRequestDuration": True,
        "docExpansion": "list",
        "filter": True,
        "operationsSorter": "alpha",
        "showExtensions": True,
        "tagsSorter": "alpha",
    }

    SWAGGER_META: dict = {
        "title": "FastAPI",
        "version": "0.1.0",
        "description": "## API by FastAPI",
        "contact": {
            "name": "Hello World",
            "url": "https://github.com",
            "email": "example@gmail.com",
            "license_info": {
                "name": "",
                "url": "",
            },
        },
    }

    LOG_CONFIG: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(levelname)s [%(name)s:%(lineno)s] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "information": {
                "format": "%(levelname)s %(message)s",
            },
        },
        "handlers": {
            "default": {
                "level": "INFO",
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "default": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False,
            },
        },
    }

    SUPABASE_URL: str
    SUPABASE_KEY: str

    @property
    def TIMEZONE(self) -> ZoneInfo:
        return ZoneInfo(self.TIMEZONE_LOCATION)


settings = AppSettings()
