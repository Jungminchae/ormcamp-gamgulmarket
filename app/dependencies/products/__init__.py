from fastapi_mctools.dependencies import Dependency
from app.dependencies.products.products import create_product, update_product, read_products, retrieve_product, remove_product

product_dependency = Dependency(
    CreateProduct=create_product,
    UpdateProduct=update_product,
    ReadProducts=read_products,
    RetrieveProduct=retrieve_product,
    RemoveProduct=remove_product,
)
