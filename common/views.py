from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def custom_404(request, exception):
    if "application/json" in request.headers.get("Accept", ""):
        return JsonResponse({
            "error": "Not found",
            "status_code": 404,
            "detail": "The requested resource was not found",
            }, status=404)
    else:
        return render(request, "common/404.html", status=404)
    

def api_not_found(request):
    return JsonResponse({
        "error": "Not found",
        "status_code": 404,
        "detail": "The requested resource was not found",
    }, status=404)