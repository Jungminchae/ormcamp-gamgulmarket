from fastapi import APIRouter, status
from fastapi_mctools.utils.responses import ResponseInterFace
from app.dependencies.products import product_dependency


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(data: product_dependency.CreateProduct):
    """
    # 상품 등록
    감귤 마켓에 상품을 등록하는 API 입니다.
    - **name**: 상품명
    - **price**: 가격
    - **description**: 설명
    """
    response = ResponseInterFace(result=data, message="상품 생성 완료")
    return response


@router.put("/{product_id}/", status_code=status.HTTP_200_OK)
async def update_product(data: product_dependency.UpdateProduct):
    """
    # 상품 수정
    감귤 마켓에 상품을 수정하는 API 입니다.
    - 모든 필드 optional이지만, 최소 하나의 필드는 수정해야 합니다.
    """
    response = ResponseInterFace(result=data, message="상품 수정 완료")
    return response
