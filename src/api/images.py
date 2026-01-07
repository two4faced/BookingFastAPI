from fastapi import APIRouter, UploadFile

from src.services.images import ImagesService

router = APIRouter(prefix='/images', tags=['Изображения'])


@router.post('')
def add_image(file: UploadFile):
    ImagesService().add_image(file)
