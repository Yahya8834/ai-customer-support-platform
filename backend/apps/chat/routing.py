from django.urls import path
from apps.chat.consumers import ChatConsumer



websocket_urlpatterns = [
    path(
        "ws/v1/chat/",
        ChatConsumer.as_asgi(),
    ),
]