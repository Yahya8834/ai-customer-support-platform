from celery import shared_task
from django.conf import settings
from apps.common.integrations.ai_service.client import AIServiceClient



@shared_task
def process_chat_message(
    workspace_uuid: str,
    provider: str,
    model: str,
    prompt: str,
) -> None:

    print(">>> CELERY TASK STARTED <<<", flush=True)

    client = AIServiceClient(
        settings.AI_SERVICE_URL,
    )

    for chunk in client.chat_stream(
        workspace_uuid=workspace_uuid,
        provider=provider,
        model=model,
        prompt=prompt,
    ):
        print(repr(chunk), flush=True)