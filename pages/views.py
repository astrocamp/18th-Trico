from django.shortcuts import render
from services.models import Service, Category


def home(request):
    categories = Category.objects.prefetch_related("services")
    services = Service.objects.order_by("-created_at")[:4]
    placeholders = max(0, 4 - services.count())
    return render(request, "pages/home.html", {"services": services, "categories": categories, "placeholders": range(placeholders)})


def portfolio_showcase(request):
    return render(request, "pages/portfolio_showcase.html")

def client(request):
    return render(request, "pages/client.html")

def freelancer(request):
    return render(request, "pages/freelancer.html")
