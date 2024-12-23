from django.urls import path
from .views import all_services, service_by_category

app_name = "categories"

urlpatterns = [
    path("", all_services, name="all_categories"),
    path("<int:id>/", service_by_category, name="service_by_category"),
]