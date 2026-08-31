from django.db.models import QuerySet
from apps.chat.models.conversation import Conversation



def list_workspace_conversations(
    workspace_uuid,
) -> QuerySet[Conversation]:
    return Conversation.objects.filter(
        workspace_id=workspace_uuid,
    )