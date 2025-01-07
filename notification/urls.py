from django.urls import path
from .views import notifications_unread, mark_notification_as_read

urlpatterns = [
    path("unread/", notifications_unread, name="notifications_unread"),
    path(
        "mark-as-read/<int:notification_id>/",
        mark_notification_as_read,
        name="mark_notification_as_read",
    ),
]
