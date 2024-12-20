from django.urls import path
from .views import home, portfolio_showcase
from .views import home, client, freelancer, searchpage

app_name = "pages"

urlpatterns = [
    path("", home, name="home"),
    path("portfolio_showcase/", portfolio_showcase, name="portfolio_showcase"),
<<<<<<< HEAD
    path("client/", client, name="client"),
    path("freelancer/", freelancer, name="freelancer"),
    path("searchpage/", searchpage, name="searchpage"),
=======
<<<<<<< HEAD
=======
    path("client/", client, name="client"),
    path("freelancer/", freelancer, name="freelancer"),
    path("searchpage/", searchpage, name="searchpage"),
>>>>>>> 8cbe19e (wip: searchpage)
>>>>>>> bdfd8fb (fix: rebase conflict)
]
