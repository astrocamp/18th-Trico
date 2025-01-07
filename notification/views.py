from django.shortcuts import render
from .models import Notification
from django.http import JsonResponse


def notifications_unread(request):
    if not request.user.is_authenticated:
        return render(request, "notification/unread.html", {"unread_notifications": []})

    unread_notifications = request.user.notifications.filter(unread=True)
    return render(
        request,
        "notification/unread.html",
        {
            "unread_notifications": unread_notifications,
        },
    )


def mark_notification_as_read(request, notification_id):
    if request.user.is_authenticated:
        notification = Notification.objects.filter(
            id=notification_id, recipient=request.user
        ).first()
        if notification:
            notification.unread = False
            notification.save()
            return JsonResponse({"status": "success"})
    return JsonResponse({"status": "unauthorized"}, status=401)
