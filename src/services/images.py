import os
import shutil

from fastapi import UploadFile

from src.services.base import BaseService
from src.tasks.tasks import resize_hotel_image


class ImagesService(BaseService):
    def add_hotel_image(self, file: UploadFile, hotel_id: int):
        if not os.path.isdir(f'src/static/images/{hotel_id}'):
            os.mkdir(f'src/static/images/{hotel_id}')
        image_path = f'src/static/images/{hotel_id}/{file.filename}'
        with open(image_path, 'wb+') as new_file:
            shutil.copyfileobj(file.file, new_file)

        # resize_hotel_image.delay(image_path, hotel_id)

        return image_path

    def add_room_image(self, file: UploadFile, hotel_id: int, room_id: int):
        if not os.path.isdir(f'src/static/images/{hotel_id}/{room_id}'):
            os.mkdir(f'src/static/images/{hotel_id}/{room_id}')
        image_path = f'src/static/images/{hotel_id}/{room_id}/{file.filename}'
        with open(image_path, 'wb+') as new_file:
            shutil.copyfileobj(file.file, new_file)

        return image_path
