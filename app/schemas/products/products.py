from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str
    price: int
    citrus_variety: str | None = None
    cultivation_region: str | None = None
    harvest_time: str | None = None
    image_urls: list[str] | None = None
    created_at: datetime
    updated_at: datetime | None = None


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total: int
    page: int
    data: list[ProductRead]
