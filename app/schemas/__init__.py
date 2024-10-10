from pydantic import BaseModel


class BaseResponse(BaseModel):
    result: dict
    message: str


class ListResponse(BaseModel):
    result: list
    message: str
