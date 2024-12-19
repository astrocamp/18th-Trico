from django.urls import path
from .views import register, login, logout, profile,user_dashboard,apply_freelancer,switch_role

app_name = "users"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("profile/", profile, name="profile"),
    path("", user_dashboard, name="user_dashboard"),
    path("apply", apply_freelancer, name="apply_freelancer"),
    path("switch_role", switch_role, name="switch_role")
]

