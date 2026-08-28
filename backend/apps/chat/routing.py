from django.urls import path

from apps.chat.consumers import ChatConsumer


websocket_urlpatterns = [
    path(
        "ws/v1/chat/<uuid:workspace_uuid>/",
        ChatConsumer.as_asgi(),
    ),
]