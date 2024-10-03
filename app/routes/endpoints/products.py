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
