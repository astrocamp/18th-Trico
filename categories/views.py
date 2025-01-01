from django.shortcuts import render, get_object_or_404
from services.models import Service, Category


# Create your views here.


def all_services(request):
    services = Service.objects.all()
    return render(request, "categories/all_services.html", {"services": services})


def service_by_category(request, id):
    category = get_object_or_404(Category, id=id)
    services = Service.objects.filter(category__id=id)
    return render(
        request,
        "categories/service_by_category.html",
        {"services": services, "category": category},
    )
