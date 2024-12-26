from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pages.urls")),
    path("users/", include("users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    path("order/", include("order.urls")),
    path("services/", include("services.urls")),
    path("categories/", include("categories.urls")),
    path("comments/", include("comments.urls")),
]
