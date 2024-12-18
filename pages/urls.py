from django.urls import path
from .views import home, portfolio_showcase
from .views import home, client, freelancer

app_name = "pages"

urlpatterns = [
    path("", home, name="home"),
    path("portfolio_showcase/", portfolio_showcase, name="portfolio_showcase"),
]
