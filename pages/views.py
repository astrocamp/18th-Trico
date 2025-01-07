from django.db.models import Avg
from django.shortcuts import render
from services.models import Service, Like, Category
from notification.models import Notification


def home(request):
    categories = Category.objects.prefetch_related("services")
    services = Service.objects.order_by("-created_at").annotate(
        average_rating=Avg("comments__rating")
    )[:4]

    # 判斷每個服務是否已被當前用戶點擊愛心
    for service in services:
        if request.user.is_authenticated:
            service.is_liked = Like.objects.filter(
                user=request.user, service=service
            ).exists()
        else:
            service.is_liked = False

    placeholders = max(0, 4 - services.count())

    # 未讀通知列表
    unread_notifications = []
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(
            recipient=request.user, unread=True
        ).order_by("-timestamp")

    return render(
        request,
        "pages/home.html",
        {
            "services": services,
            "categories": categories,
            "placeholders": range(placeholders),
            "unread_notifications": unread_notifications,  # 傳遞未讀通知到模板
        },
    )

def portfolio_showcase(request):
    return render(request, "pages/portfolio_showcase.html")


def client(request):
    return render(request, "pages/client.html")


def freelancer(request):
    return render(request, "pages/freelancer.html")


def about_page(request):
    return render(request, "pages/about.html")
