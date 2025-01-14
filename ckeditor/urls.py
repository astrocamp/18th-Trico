from django.urls import path
from ckeditor.views import *
from ckeditor.views import file_upload_view, file_browse_view

app_name="ckeditor"
urlpatterns = [
    path("ckeditor5/upload/", file_upload_view, name="ckeditor5_upload"),
    path("ckeditor5/browse/", file_browse_view, name="ckeditor5_browse"),  # 文件瀏覽
]




