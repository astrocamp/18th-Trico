from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpattern = [
    re_path(r'ws/chat/(?P<user_id>\w+/$)', ChatConsumer.as_asgi())
]