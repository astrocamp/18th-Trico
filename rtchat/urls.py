from django.urls import path
from .views import *

urlpatterns = [
    path("", chat_view, name="home"),
    # path('chat/', chat_view),
    # path('chat/<str:room_name>/', chat_view),
]



