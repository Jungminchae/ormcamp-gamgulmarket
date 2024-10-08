from sqlalchemy import select, delete, func
from fastapi_mctools.orms.sqlalchemy import async_base
from app.models.products import Product


class ProductCreate(async_base.ACreateBase): ...


class ProductRead(async_base.AReadBase):
    async def get_products_by_keyword_similarity(self, db, keyword, page, page_size):
        if keyword is None:
            query = select(self.model)
        else:
            query = (
                select(self.model)
                .where(
                    (func.similarity(self.model.name, keyword) >= 0.3) | (func.similarity(self.model.description, keyword) >= 0.3)
                )
                .order_by(
                    func.greatest(
                        func.similarity(self.model.name, keyword), func.similarity(self.model.description, keyword)
                    ).desc()
                )
            )

        if page and page:
            query = query.limit(page_size).offset((page - 1) * page_size)

        results = await db.execute(query)
        results = self.get_results(results, [])
        results = [result[self.model_name] for result in results]

        return results

    async def get_count(self, db):
        query = select(func.count(self.model.id).label("count"))
        result = await db.execute(query)
        return self.get_result(result, ["count"])


class ProductUpdate(async_base.AUpdateBase): ...


class ProductDelete(async_base.ADeleteBase):
    async def delete_product(self, db, product_id):
        query = delete(self.model).where(self.model.id == product_id)
        await db.execute(query)
        await db.commit()
        return


class ProductORM(ProductCreate, ProductRead, ProductUpdate, ProductDelete):
    def __init__(self, model):
        self.model_name = "Product"
        super().__init__(model)


product_orm = ProductORM(Product)
