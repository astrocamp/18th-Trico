from django.urls import re_path
from web.Consumers.consumers import ChatConsumer

websoket_urlpatterns = [
    re_path(r'chat/', ChatConsumer.as_asgi()),
]