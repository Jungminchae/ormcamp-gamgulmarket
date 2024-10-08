import os
from typing import Annotated, TYPE_CHECKING, NoReturn
from collections import namedtuple
from fastapi import Depends, Query, UploadFile, File, Form, status
from fastapi.encoders import jsonable_encoder
from fastapi_mctools.exceptions import HTTPException
from app.db.async_session import DB
from app.services.core import images
from app.orms.products import product_orm
from app.schemas.params import PageParams
from app.schemas.products import ProductResponse
from app.dependencies.permissions import permission_dependency
from app.dependencies.authentication import auth_dependency
from app.config.settings import settings

if TYPE_CHECKING:
    from app.models.products import Product


async def create_product(
    db: DB,
    user: auth_dependency.CurrentUser,
    image_files: Annotated[list[UploadFile], File()],
    name: Annotated[str, Form(...)],
    price: Annotated[int, Form(...)],
    description: Annotated[str, Form(...)],
    citrus_variety: Annotated[str | None, Form(...)] = None,
    cultivation_region: Annotated[str | None, Form(...)] = None,
    harvest_time: Annotated[str | None, Form(...)] = None,
) -> "Product":
    """
    로그인 된 유저만 상품 등록 가능
    """
    validated_image_urls = []
    for file in image_files:
        if not file:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미지 없음", code="NO_IMAGE")

        file = await images.validate_image_type(file)
        file = await images.validate_image_size(file)
        file = images.change_filename(file)
        filename = file.filename
        image = images.resize_image(file)
        # FIXME: 파일시스템에 저장했다가 지우는 방법은 좋지 않음 -> 애초에 미니 프로젝트가 아니면 Supabase Storage를 사용하지 않음
        images.save_image_to_filesystem(image, f"./{filename}")
        with open(f"./{filename}", "rb") as f:
            images.upload_image_to_supabase(f, "gamgul", filename)
            os.remove(f"./{filename}")
            # TODO: image 저장 필드를 JSONB로 변경해야겠음
            validated_image_urls.append(f"{settings.SUPABASE_URL}/gamgul/{filename}")

    data = {
        "user_id": user.id,
        "name": name,
        "price": price,
        "description": description,
        "citrus_variety": citrus_variety,
        "cultivation_region": cultivation_region,
        "harvest_time": harvest_time,
        "image_urls": validated_image_urls,
    }

    product = await product_orm.create(db, **data)
    product = jsonable_encoder(product)
    return product


async def update_product(
    db: DB,
    product_id: int,
    user: permission_dependency.IsProductOwner,
    image_files: Annotated[list[UploadFile] | None, File()],
    name: Annotated[str | None, Form(...)],
    price: Annotated[int | None, Form(...)],
    description: Annotated[str | None, Form(...)],
    citrus_variety: Annotated[str | None, Form(...)],
    cultivation_region: Annotated[str | None, Form(...)],
    harvest_time: Annotated[str | None, Form(...)],
) -> dict:
    """
    상품 수정
    """

    data = {}
    if image_files:
        validated_image_urls = []
        for file in image_files:
            if not file:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미지 없음", code="NO_IMAGE")

            file = await images.validate_image_type(file)
            file = await images.validate_image_size(file)
            file = images.change_filename(file)
            filename = file.filename
            image = images.resize_image(file)
            images.save_image_to_filesystem(image, f"./{filename}")
            with open(f"./{filename}", "rb") as f:
                images.upload_image_to_supabase(f, "gamgul", filename)
                os.remove(f"./{filename}")
                validated_image_urls.append(f"{settings.SUPABASE_URL}/gamgul/{filename}")
        data["image_urls"] = validated_image_urls

    fields = [
        namedtuple("Field", ["key", "value"])("name", name),
        namedtuple("Field", ["key", "value"])("price", price),
        namedtuple("Field", ["key", "value"])("description", description),
        namedtuple("Field", ["key", "value"])("citrus_variety", citrus_variety),
        namedtuple("Field", ["key", "value"])("cultivation_region", cultivation_region),
        namedtuple("Field", ["key", "value"])("harvest_time", harvest_time),
    ]

    for field in fields:
        if field.value:
            data[field.key] = field.value

    if not data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="수정할 내용이 없습니다.", code="NO_CONTENT")

    await product_orm.update_by_id(db, product_id, **data)

    return data


async def remove_product(
    db: DB,
    product_id: int,
    user: permission_dependency.IsProductOwner,
) -> NoReturn:
    """
    상품 삭제
    TODO: 삭제 같은 경우 데이터베이스에서 삭제할 때 Storage에 저장된 이미지를 삭제해야 할 수 있음
    """
    await product_orm.delete_product(db, product_id)
    return


async def read_products(
    db: DB,
    keyword: Annotated[str | None, Query()] = None,
    page_params: PageParams = Depends(),
) -> list["Product"]:
    """
    상품 리스트 조회
    """
    products = await product_orm.get_products_by_keyword_similarity(
        db, keyword=keyword, page=page_params.page, page_size=page_params.page_size
    )
    count = await product_orm.get_count(db)

    products = ProductResponse(total=count, page=page_params.page, data=products)
    return products


async def retrieve_product(
    db: DB,
    product_id: int,
) -> dict:
    """
    상품 상세 조회
    """

    product = await product_orm.get_by_id(db, product_id)
    product = jsonable_encoder(product) if product else {}
    return product
