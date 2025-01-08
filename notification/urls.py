from django.urls import path
from . import views

app_name = "notification"  

urlpatterns = [
    path("unread/", views.notifications_unread, name="notifications_unread"),
    path(
        "mark-as-read/<int:notification_id>/",
        views.mark_notification_as_read,
        name="mark_as_read",
    ),
    path(
        "mark-as-read-and-redirect/<int:notification_id>/",
        views.mark_as_read_and_redirect,
        name="mark_as_read_and_redirect",
    ),
    path(
        "unread-count/",
        views.unread_notifications_count,
        name="unread_notifications_count",
    ),
]
