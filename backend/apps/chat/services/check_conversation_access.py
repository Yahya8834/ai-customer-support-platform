from django.core.exceptions import PermissionDenied
from apps.chat.models.conversation import Conversation



def check_conversation_access(*, conversation_uuid, workspace_uuid):
    conversation_exists = Conversation.objects.filter(
        uuid=conversation_uuid,
        workspace_id=workspace_uuid,
    ).exists()

    if not conversation_exists:
        raise PermissionDenied(
            "Conversation does not belong to this workspace."
        )

    return True