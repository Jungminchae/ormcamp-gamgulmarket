from pydantic import BaseModel


class ProfileUpdateRequest(BaseModel):
    profile: dict
