from django.shortcuts import render
from django.db.models import Q
from services.models import Service
from .forms import SearchForm
from services.models import Service
from django.shortcuts import get_object_or_404
from .models import Search  # 添加這行

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
            # 過濾標題或內容中包含關鍵字的結果
            results = Service.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            ).all()  # 確保獲取所有結果
    else:
        form = SearchForm()

    return render(
        request, "search.html", 
        {
            "form": form, 
            "query": query, 
            "results": results
        }
    )