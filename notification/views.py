from django.shortcuts import redirect, render
from .models import Notification
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import Http404


# 顯示未讀通知
@login_required
def notifications_unread(request):
    unread_notifications = request.user.notifications.filter(unread=True)
    return render(
        request,
        "notification/unread.html",
        {"unread_notifications": unread_notifications},
    )


# 標記單個通知為已讀並返回剩餘未讀數量
@login_required
def mark_notification_as_read(request, notification_id):
    if request.user.is_authenticated:
        notification = Notification.objects.filter(
            id=notification_id, recipient=request.user
        ).first()
        if notification:
            notification.unread = False
            notification.save()

            # 計算未讀通知數量
            unread_count = Notification.objects.filter(
                recipient=request.user, unread=True
            ).count()

            return JsonResponse({"status": "success", "unread_count": unread_count})
    return JsonResponse({"status": "unauthorized"}, status=401)


# 返回未讀通知數量，純數字
@login_required
def unread_notifications_count(request):
    count = request.user.notifications.filter(unread=True).count()
    return HttpResponse(count, content_type="text/plain")  # 返回純數字


@login_required
def mark_as_read_and_redirect(request, notification_id):
    try:
        notification = Notification.objects.get(
            id=notification_id, recipient=request.user
        )
        notification.unread = False
        notification.save()
        # 重定向到目標 URL
        return redirect(notification.get_target_url())
    except Notification.DoesNotExist:
        raise Http404("Notification not found")
