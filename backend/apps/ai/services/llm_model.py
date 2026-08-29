from apps.ai.models import LLMModel


class ActiveLLMModelService:
    @staticmethod
    def get_active_model() -> LLMModel:
        try:
            return LLMModel.objects.get(is_active=True)
        except LLMModel.DoesNotExist:
            raise LLMModel.DoesNotExist(
                "No active LLM model is configured."
            )
        except LLMModel.MultipleObjectsReturned:
            raise LLMModel.MultipleObjectsReturned(
                "Multiple active LLM models are configured."
            )