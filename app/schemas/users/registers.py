from pydantic import BaseModel, model_validator, field_validator


class RegisterUserRequest(BaseModel):
    email: str | None = None
    password: str | None = None
    password_confirmation: str = None

    @field_validator("password")
    @classmethod
    def validate(cls, value):
        if len(value) < 8:
            raise ValueError("비밀번호는 8자 이상이어야 합니다.")
        if not any(char.isdigit() for char in value):
            raise ValueError("비밀번호는 숫자를 포함해야 합니다.")
        if not any(char.isalpha() for char in value):
            raise ValueError("비밀번호는 문자를 포함해야 합니다.")
        if not any(char.isupper() for char in value):
            raise ValueError("비밀번호는 대문자를 포함해야 합니다.")

        return value

    @model_validator(mode="before")
    @classmethod
    def validate_password(cls, data):
        password = data.get("password")
        password_confirmation = data.get("password_confirmation")

        if password != password_confirmation:
            raise ValueError("비밀번호 확인이 일치하지 않습니다.")
        return data
