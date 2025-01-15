from django.shortcuts import render
from django.db.models import Q
from services.models import Service
from .forms import SearchForm
from services.models import Service
from django.shortcuts import get_object_or_404
from .models import Search  # 添加這行
from services.models import Like


def service_detail_view(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, "services/service_detail.html", {"service": service})


def search_view(request):
    query = None
    results = []
    if "keyword" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["keyword"]
            results = (
                Service.objects.filter(
                    Q(title__icontains=query)
                    | Q(description__icontains=query)
                    | Q(standard_description__icontains=query)
                    | Q(premium_description__icontains=query)
                )
                .select_related("freelancer_user")
                .all()
            )
            for service in results:
                if request.user.is_authenticated:
                    service.is_liked = Like.objects.filter(
                        user=request.user, service=service
                    ).exists()
                else:
                    service.is_liked = False
    else:
        form = SearchForm()

    return render(
        request, "search.html", {"form": form, "query": query, "results": results}
    )
