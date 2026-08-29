from unittest.mock import Mock, patch
from django.test import TestCase
from apps.ai.models import LLMModel
from apps.ai.services.answer_question import AnswerQuestionService
from apps.common.exceptions import AIServiceError




class AnswerQuestionServiceTests(TestCase):

    @patch("apps.ai.services.answer_question.AIServiceClient")
    def test_generates_answer_using_active_model(
        self,
        mock_client_class,
    ):
        LLMModel.objects.create(
            key="local-deepseek",
            display_name="DeepSeek R1 8B",
            description="Local DeepSeek R1 8B model.",
            strength="Reasoning",
            provider="ollama",
            model_name="deepseek-r1:8b",
            is_active=True,
        )

        mock_client = Mock()
        mock_client.chat.return_value = "Password reset instructions."
        mock_client_class.return_value = mock_client

        service = AnswerQuestionService()

        result = service.execute(
            workspace_uuid="550e8400-e29b-41d4-a716-446655440000",
            prompt="How do I reset my password?",
        )

        self.assertEqual(
            result,
            "Password reset instructions.",
        )

        mock_client.chat.assert_called_once_with(
            workspace_uuid="550e8400-e29b-41d4-a716-446655440000",
            provider="ollama",
            model="deepseek-r1:8b",
            prompt="How do I reset my password?",
        )



    def test_generates_answer_using_active_qwen_model(self):
        LLMModel.objects.create(
            key="cloud-qwen",
            display_name="Qwen 3.5 397B A17B",
            description="Cloud Qwen model.",
            strength="General purpose",
            provider="qwen",
            model_name="qwen3.5-397b-a17b",
            is_active=True,
        )

        ai_service_client = Mock()
        ai_service_client.chat.return_value = (
            "The answer from Qwen."
        )

        service = AnswerQuestionService(
            ai_service_client=ai_service_client,
        )

        result = service.execute(
            workspace_uuid="550e8400-e29b-41d4-a716-446655440000",
            prompt="What is the refund policy?",
        )

        self.assertEqual(
            result,
            "The answer from Qwen.",
        )

        ai_service_client.chat.assert_called_once_with(
            workspace_uuid="550e8400-e29b-41d4-a716-446655440000",
            provider="qwen",
            model="qwen3.5-397b-a17b",
            prompt="What is the refund policy?",
        )

    
    def test_raises_when_no_active_model_exists(self):
        ai_service_client = Mock()

        service = AnswerQuestionService(
            ai_service_client=ai_service_client,
        )

        with self.assertRaisesMessage(
            LLMModel.DoesNotExist,
            "No active LLM model is configured.",
        ):
            service.execute(
                workspace_uuid="550e8400-e29b-41d4-a716-446655440000",
                prompt="How do I reset my password?",
            )

        ai_service_client.chat.assert_not_called()


    
    def test_propagates_ai_service_error(self):
        LLMModel.objects.create(
            key="local-deepseek",
            display_name="DeepSeek R1 8B",
            description="Local DeepSeek R1 8B model.",
            strength="Reasoning",
            provider="ollama",
            model_name="deepseek-r1:8b",
            is_active=True,
        )

        ai_service_client = Mock()
        ai_service_client.chat.side_effect = AIServiceError(
            "AI service unavailable."
        )

        service = AnswerQuestionService(
            ai_service_client=ai_service_client,
        )

        with self.assertRaisesMessage(
            AIServiceError,
            "AI service unavailable.",
        ):
            service.execute(
                workspace_uuid="550e8400-e29b-41d4-a716-446655440000",
                prompt="How do I reset my password?",
            )