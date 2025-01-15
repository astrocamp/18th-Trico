from django.urls import path, re_path
from .views import *
app_name = "rtchat"  

urlpatterns = [
    path("", chat_view, name="home"),
    path("chat/room/<chatroom_name>/", chat_view, name="chatroom"),
    re_path(r"^chat/(?P<username>[\w.@+-]+)/$", get_or_create_chatroom, name="start-chat"),
    path("unread/notifications/chat/", unread_notifications_count_chat, name="unread_notifications_count_chat"),

]
