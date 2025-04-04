import os
import shutil
from fastapi import APIRouter, UploadFile

from src.tasks.celery_tasks import resize_image

router = APIRouter(prefix="/images", tags=["Images"])


@router.post("")
def upload_image(image: UploadFile):
    file_name, ext = os.path.splitext(image.filename)
    image_dir = f"src/static/img/{file_name}"
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    image_path = f"{image_dir}/{image.filename}"
    with open(image_path, "wb") as new_file:
        shutil.copyfileobj(image.file, new_file)

    resize_image.delay(image_path)
