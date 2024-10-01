import pytest
from fastapi_mctools.test_tools.db_managers import TestConfDBManager
from app.models.base import Base
from app.config.settings import settings
from app.orms.users import user_orm


db_test_manager = TestConfDBManager(settings.TEST_DB_URL)


@pytest.fixture
async def db():
    async for session in db_test_manager.get_async_db_session(base=Base, is_meta=True):
        yield session


@pytest.fixture
async def sample_user(db):
    user = await user_orm.create(db, email="test@example.com", password="Password123")
    return user
