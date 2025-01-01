from django.urls import path
from .views import home, portfolio_showcase, client, freelancer, about_page

app_name = "pages"

urlpatterns = [
    path("", home, name="home"),
    path("portfolio_showcase/", portfolio_showcase, name="portfolio_showcase"),
    path("client/", client, name="client"),
    path("freelancer/", freelancer, name="freelancer"),
    path("about/", about_page, name="about"),
]
