from django.test import TestCase
from apps.ai.models import LLMModel
from apps.ai.services.llm_model import ActiveLLMModelService



class ActiveLLMModelServiceTest(TestCase):
    def test_get_active_model_returns_active_model(self):
        LLMModel.objects.create(
            key="local-deepseek",
            display_name="DeepSeek R1 8B",
            description="Local DeepSeek R1 8B model.",
            strength="Reasoning",
            provider="ollama",
            model_name="deepseek-r1:8b",
            is_active=True,
        )

        model = ActiveLLMModelService.get_active_model()

        self.assertEqual(model.key, "local-deepseek")
        self.assertEqual(model.provider, "ollama")
        self.assertEqual(model.model_name, "deepseek-r1:8b")



    def test_get_active_model_raises_when_no_active_model_exists(self):
        with self.assertRaises(LLMModel.DoesNotExist):
            ActiveLLMModelService.get_active_model()


    
    def test_get_active_model_returns_provider_configuration(self):
        LLMModel.objects.create(
            key="cloud-qwen",
            display_name="Qwen 3.5 397B A17B",
            description="Cloud Qwen model.",
            strength="General purpose",
            provider="qwen",
            model_name="qwen3.5-397b-a17b",
            is_active=True,
        )

        model = ActiveLLMModelService.get_active_model()

        self.assertEqual(model.provider, "qwen")
        self.assertEqual(model.model_name, "qwen3.5-397b-a17b")


    
    def test_get_active_model_raises_clear_error_when_none_exists(self):
        with self.assertRaisesMessage(
            LLMModel.DoesNotExist,
            "No active LLM model is configured.",
        ):
            ActiveLLMModelService.get_active_model()


