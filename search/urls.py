from django.urls import path
from . import views

urlpatterns = [
    path("search", views.search_view, name="search"), 
    path("service/<int:pk>/", views.service_detail_view, name="service_detail")
]
