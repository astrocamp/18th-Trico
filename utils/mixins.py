from django.db import models
from utils.image_processing import convert_and_upload_to_webp
import boto3
from django.conf import settings

class WebPImageModelMixin(models.Model):
    """
    用於將圖片轉換為 WebP 格式並上傳到 S3 的 mixin
    """

    class Meta:
        abstract = True

    def process_and_upload_image(self, image_file, folder_name):
        """
        將圖片轉換為 WebP 格式並上傳到 S3，同時清理原始圖片。

        參數：
        - image_file: 要處理的圖片檔案
        - original_filename: 原始圖片檔案名稱

        返回：
        - none
        """
        original_filename = image_file.name
        new_image_path = convert_and_upload_to_webp(image_file, folder_name)
        image_file.name = new_image_path

        # 從 S3 中刪除原始文件
        if original_filename:
            s3 = boto3.client("s3", region_name=settings.AWS_S3_REGION_NAME)
            s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=original_filename)