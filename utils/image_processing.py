from PIL import Image
from io import BytesIO
import boto3
import logging
import uuid
from django.conf import settings

def convert_and_upload_to_webp(photo, folder_name):
    try:
        image = Image.open(photo)

        webp_image_io = BytesIO()
        image.save(webp_image_io, format="WEBP", quality=85)
        webp_image_io.seek(0)

        unique_filename = f"{folder_name}/{uuid.uuid4()}.webp"

        s3 = boto3.client("s3", region_name=settings.AWS_S3_REGION_NAME)
        s3.upload_fileobj(
            webp_image_io,
            settings.AWS_STORAGE_BUCKET_NAME,
            unique_filename,
            ExtraArgs={"ContentType": "image/webp"},
        )

        return unique_filename

    except Exception as e:
        logging.error(f"Error converting image to webp: {e}")
        return folder_name