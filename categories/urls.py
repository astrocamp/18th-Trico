from django.urls import path
from .views import all, category,tag

app_name = "categories"

urlpatterns = [
    path("", all, name="all"),
    path("tag/<str:tag_name>/", tag, name="tag"),
    path("<int:id>/", category, name="category"),
    
]

