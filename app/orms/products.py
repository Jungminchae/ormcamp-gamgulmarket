from fastapi_mctools.orms.sqlalchemy import async_base
from app.models.products import Product


class ProductCreate(async_base.ACreateBase): ...


class ProductRead(async_base.AReadBase): ...


class ProductUpdate(async_base.AUpdateBase): ...


class ProductDelete(async_base.ADeleteBase): ...


class ProductORM(ProductCreate, ProductRead, ProductUpdate, ProductDelete):
    def __init__(self, model):
        super().__init__(model)


product_orm = ProductORM(Product)
