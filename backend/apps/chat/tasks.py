from celery import shared_task
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from apps.common.integrations.ai_service.client import AIServiceClient


@shared_task
def process_chat_message(
    workspace_uuid: str,
    provider: str,
    model: str,
    prompt: str,
) -> None:
    
    client = AIServiceClient(
        settings.AI_SERVICE_URL,
    )

    channel_layer = get_channel_layer()
    group_name = f"workspace_{workspace_uuid}"

    print(f">>> CELERY GROUP: {group_name}", flush=True)
    print(f">>> CHANNEL LAYER: {channel_layer}", flush=True)

    for chunk in client.chat_stream(
        workspace_uuid=workspace_uuid,
        provider=provider,
        model=model,
        prompt=prompt,
    ):
        print(f">>> SENDING TOKEN: {chunk!r}", flush=True)
        
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "chat_message",
                "token": chunk,
            },

            
        )