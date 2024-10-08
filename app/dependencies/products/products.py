import os
from typing import Annotated, TYPE_CHECKING
from collections import namedtuple
from fastapi import Depends, UploadFile, File, Form, status
from fastapi.encoders import jsonable_encoder
from fastapi_mctools.exceptions import HTTPException
from app.db.async_session import DB
from app.services.core import images
from app.orms.products import product_orm
from app.schemas.params import PageParams
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
    citrus_variety: Annotated[str | None, Form(...)],
    cultivation_region: Annotated[str | None, Form(...)],
    harvest_time: Annotated[str | None, Form(...)],
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


async def read_products(
    db: DB,
    page_params: PageParams = Depends(),
) -> list["Product"]:
    """
    상품 리스트 조회
    """
    products = await product_orm.get_by_filters(db, page=page_params.page, page_size=page_params.page_size)
    return products
