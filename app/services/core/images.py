"""
이미지 처리에 관련된 함수 정의
- 이미지 타입 검증
- 이미지 크기 검증
- 이미지 파일명 변경
- 이미지 크기 조정
- 이미지 저장
"""

import io
import secrets
from supabase import create_client, Client
from PIL import Image, ImageOps
from fastapi import UploadFile, status
from fastapi_mctools.exceptions import HTTPException
from app.config.settings import settings

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


async def validate_image_type(file: UploadFile) -> UploadFile:
    if file.filename.split(".")[-1].lower() not in ["jpg", "jpeg", "png"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="업로드 불가능한 이미지 확장자입니다.",
            code="INVALID_IMAGE_EXTENSION",
        )

    if not file.content_type.startswith("image"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미지 파일만 업로드 가능합니다.",
            code="INVALID_IMAGE_TYPE",
        )
    return file


async def validate_image_size(file: UploadFile) -> UploadFile:
    if len(await file.read()) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미지 파일은 10MB 이하만 업로드 가능합니다.",
            code="INVALID_IMAGE_SIZE",
        )
    return file


def change_filename(file: UploadFile) -> UploadFile:
    random_name = secrets.token_urlsafe(16)
    file.filename = f"{random_name}.jpeg"
    return file


def resize_image(file: UploadFile, max_size: int = 1024):
    read_image = Image.open(file.file)
    original_width, original_height = read_image.size

    if original_width > max_size or original_height > max_size:
        if original_width > original_height:
            new_width = max_size
            new_height = int((new_width / original_width) * original_height)
        else:
            new_height = max_size
            new_width = int((new_height / original_height) * original_width)
        read_image = read_image.resize((new_width, new_height))

    read_image = read_image.convert("RGB")
    read_image = ImageOps.exif_transpose(read_image)
    return read_image


def save_image_to_filesystem(image: Image, file_path: str):
    image.save(file_path, "jpeg", quality=70)
    return file_path


def upload_image_to_supabase(file: io.BufferedReader, bucket_name: str, file_name: str) -> None:
    supabase.storage.from_(bucket_name).upload(file=file, path=file_name, file_options={"content-type": "image/jpeg"})
