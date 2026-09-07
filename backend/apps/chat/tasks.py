from celery import shared_task
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from apps.chat.models.message import Message
from apps.common.integrations.ai_service.client import AIServiceClient
from apps.ai.services.llm_model import ActiveLLMModelService



@shared_task
def process_chat_message(
    workspace_uuid: str,
    conversation_uuid: str,
    prompt: str,
) -> None:
    
    client = AIServiceClient(
        settings.AI_SERVICE_URL,
    )

    channel_layer = get_channel_layer()
    group_name = f"workspace_{workspace_uuid}"

    print(f">>> CELERY GROUP: {group_name}", flush=True)
    print(f">>> CHANNEL LAYER: {channel_layer}", flush=True)

    assistant_response = ""
    model = ActiveLLMModelService.get_active_model()

    for chunk in client.chat_stream(
        workspace_uuid=workspace_uuid,
        provider=model.provider,
        model=model.model_name,
        prompt=prompt,
    ):
        assistant_response += chunk
        print(f">>> SENDING TOKEN: {chunk!r}", flush=True)
        
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "chat_message",
                "token": chunk,
            },

            
        )
    
    Message.objects.create(
        conversation_id=conversation_uuid,
        role="assistant",
        content=assistant_response,
    )