from fastapi_mctools.orms.sqlalchemy import async_base
from app.models.products import Product


class ProductCreate(async_base.ACreateBase): ...


class ProductORM(ProductCreate):
    def __init__(self, model):
        super().__init__(model)


product_orm = ProductORM(Product)
