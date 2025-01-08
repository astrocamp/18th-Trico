from notification.models import Notification


def unread_notifications(request):
    if request.user.is_authenticated:
        return {
            "unread_notifications": Notification.objects.filter(
                recipient=request.user, unread=True
            )
        }
    return {"unread_notifications": []}
