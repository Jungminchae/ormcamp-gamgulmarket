from pydantic import BaseModel, model_validator


class ResignationRequest(BaseModel):
    password: str
    password_confirmation: str
    resignation_reason: str

    @model_validator(mode="before")
    @classmethod
    def validate_password(cls, data):
        password = data.get("password")
        password_confirmation = data.get("password_confirmation")

        if password != password_confirmation:
            raise ValueError("비밀번호 확인이 일치하지 않습니다.")
        return data
