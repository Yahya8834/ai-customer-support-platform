from django.db.models import QuerySet
from apps.chat.models.message import Message



def list_conversation_messages(
    conversation_uuid,
) -> QuerySet[Message]:
    return Message.objects.filter(
        conversation_id=conversation_uuid,
    )