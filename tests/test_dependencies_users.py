import pytest
from fastapi_mctools.exceptions import HTTPException
from app.dependencies.users.registers import check_email_exists, register_user_by_email
from app.schemas.users.registers import RegisterUserRequest

pytestmark = pytest.mark.asyncio


async def test_check_email_exists_이메일_존재(db, sample_user):
    data = RegisterUserRequest(email="test@example.com", password="Password123", password_confirmation="Password123")

    with pytest.raises(HTTPException):
        await check_email_exists(data, db)


async def test_check_email_exists_이메일_미존재(db):
    data = RegisterUserRequest(email="test2@example.com", password="Password123", password_confirmation="Password123")

    result = await check_email_exists(data, db)
    assert result == data


async def test_register_user_by_email(db):
    data = RegisterUserRequest(email="test@example.com", password="Password123", password_confirmation="Password123")
    result = await register_user_by_email(data, db)
    assert result.get("email") == data.email
