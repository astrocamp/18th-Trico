from django.urls import path
from .views import register, login, logout, profile,user_dashboard

app_name = "users"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("profile/", profile, name="profile"),
    path("", user_dashboard, name="user_dashboard"),
]
