from django.urls import path
from .views import custom_404, api_not_found

urlpatterns = [
    path("404/", api_not_found),  # 捕獲所有未匹配的 API 請求
]
