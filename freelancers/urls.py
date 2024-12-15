from django.urls import path
from . import views

app_name = "freelancers"
urlpatterns = [
    path("<int:id>/freelancers", views.freelancers, name="freelancers"),
]
