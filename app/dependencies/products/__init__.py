from fastapi_mctools.dependencies import Dependency
from app.dependencies.products.products import create_product

product_dependency = Dependency(
    CreateProduct=create_product,
)
