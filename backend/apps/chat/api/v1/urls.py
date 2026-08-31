from django.urls import path
from apps.chat.api.v1.views import ConversationListView, ConversationMessageListView



urlpatterns = [
    path(
        "v1/workspaces/<uuid:workspace_uuid>/conversations/",
        ConversationListView.as_view(),
        name="conversation-list",
    ),
    path(
        "v1/workspaces/<uuid:workspace_uuid>/conversations/<uuid:conversation_uuid>/messages/",
        ConversationMessageListView.as_view(),
        name="conversation-message-list",
    ),
]