import os
from typing import Annotated, TYPE_CHECKING
from fastapi import UploadFile, File, Form, status
from fastapi.encoders import jsonable_encoder
from fastapi_mctools.exceptions import HTTPException
from app.db.async_session import DB
from app.services.core import images
from app.orms.products import product_orm
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
