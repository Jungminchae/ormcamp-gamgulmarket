from fastapi import APIRouter, Depends, status
from fastapi_mctools.utils.responses import ResponseInterFace
from app.dependencies.products import product_dependency
from app.dependencies.permissions import check_product_owner_permission


router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
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


@router.put(
    "/{product_id}/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_product_owner_permission)],
)
async def update_product(data: product_dependency.UpdateProduct):
    """
    # 상품 수정
    감귤 마켓에 상품을 수정하는 API 입니다.
    - 모든 필드 optional이지만, 최소 하나의 필드는 수정해야 합니다.
    """
    response = ResponseInterFace(result=data, message="상품 수정 완료")
    return response


@router.delete(
    "/{product_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(check_product_owner_permission)],
)
async def remove_product(data: product_dependency.RemoveProduct):
    """
    # 상품 삭제
    감귤 마켓에 등록된 상품을 삭제하는 API 입니다.
    """


from fastapi.responses import ORJSONResponse, UJSONResponse  # noqa
from webtool.utils import MsgSpecJSONResponse  # noqa


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_class=MsgSpecJSONResponse,
)
async def read_products(data: product_dependency.ReadProducts):
    """
    # 상품 조회
    감귤 마켓에 등록된 상품을 조회하는 API 입니다.
    - keyword: 검색 키워드
    - page: 페이지 번호
    - page_size: 페이지 크기
    """
    response = ResponseInterFace(result=data, message="상품 조회 완료")
    return MsgSpecJSONResponse(content=response.to_dict())
    # return response


@router.get(
    "/{product_id}/",
    status_code=status.HTTP_200_OK,
)
async def retrieve_product(data: product_dependency.RetrieveProduct):
    """
    # 상품 상세 조회
    감귤 마켓에 등록된 상품을 상세 조회하는 API 입니다.
    """
    response = ResponseInterFace(result=data, message="상품 상세 조회 완료")
    return response
