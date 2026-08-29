from django.conf import settings
from apps.ai.services.llm_model import ActiveLLMModelService
from apps.common.integrations.ai_service.client import AIServiceClient



class AnswerQuestionService:

    def __init__(self, ai_service_client=None):
        self.ai_service_client = ai_service_client or AIServiceClient(
            base_url=settings.AI_SERVICE_URL,
        )

    def execute(
        self,
        *,
        workspace_uuid: str,
        prompt: str,
    ) -> str:
        model = ActiveLLMModelService.get_active_model()

        return self.ai_service_client.chat(
            workspace_uuid=workspace_uuid,
            provider=model.provider,
            model=model.model_name,
            prompt=prompt,
        )