from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str
    price: int
    citrus_variety: str | None = None
    cultivation_region: str | None = None
    harvest_time: str | None = None
