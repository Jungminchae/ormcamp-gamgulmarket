from pydantic import BaseModel


class BaseResponse(BaseModel):
    result: dict
    message: str
