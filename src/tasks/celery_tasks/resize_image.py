import logging
import os

from PIL import Image

from src.tasks.celery_app import celery_instance


@celery_instance.task
def resize_image(image_path: str):
    logging.debug(f"Calling func with image_path: {image_path}")
    sizes = [1000, 500, 200]
    output_folder = os.path.dirname(image_path)
    img = Image.open(image_path)

    base_name = os.path.basename(image_path)

    name, ext = os.path.splitext(base_name)

    for size in sizes:
        img_resized = img.resize(
            (size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS
        )

        new_file_name = f"{name}_{size}{ext}"

        output_path = os.path.join(output_folder, new_file_name)

        img_resized.save(output_path)

    logging.info(f"Images were saved in sizes:{sizes}, in a folder: {output_folder}")
