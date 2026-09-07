from unittest.mock import patch
from django.test import TestCase
from apps.chat.models.conversation import Conversation
from apps.chat.models.message import Message
from apps.ai.models import LLMModel
from apps.chat.tasks import process_chat_message
from apps.workspaces.models import Workspace



class ProcessChatMessageTests(TestCase):

    def setUp(self):
        self.workspace = Workspace.objects.create(
            name="Workspace A",
            slug="workspace-a",
        )

        self.conversation = Conversation.objects.create(
            workspace=self.workspace,
        )

    @patch("apps.chat.tasks.AIServiceClient")
    def test_assistant_response_is_persisted(
        self,
        mock_client_class,
    ):
        mock_client = mock_client_class.return_value
        mock_client.chat_stream.return_value = [
            "Hello ",
            "there!",
        ]

        LLMModel.objects.create(
            key="cloud-qwen",
            display_name="Qwen 3.5 397B A17B",
            description="Test Qwen model",
            strength="General purpose",
            provider="qwen",
            model_name="qwen3.5-397b-a17b",
            input_price_per_1k_tokens=0,
            output_price_per_1k_tokens=0,
            is_active=True,
        )

        process_chat_message(
            workspace_uuid=str(self.workspace.uuid),
            conversation_uuid=str(self.conversation.uuid),
            prompt="Hello",
        )

        message = Message.objects.get(
            conversation=self.conversation,
            role="assistant",
        )

        self.assertEqual(
            message.content,
            "Hello there!",
        )

    @patch("apps.chat.tasks.ActiveLLMModelService")
    @patch("apps.chat.tasks.AIServiceClient")
    def test_chat_uses_active_llm_model(
        self,
        mock_client_class,
        mock_model_service,
    ):
        mock_model = mock_model_service.get_active_model.return_value
        mock_model.provider = "qwen"
        mock_model.model_name = "qwen3.5-397b-a17b"

        mock_client = mock_client_class.return_value
        mock_client.chat_stream.return_value = ["Hello"]

        process_chat_message(
            workspace_uuid=str(self.workspace.uuid),
            conversation_uuid=str(self.conversation.uuid),
            prompt="Hello",
        )

        mock_client.chat_stream.assert_called_once_with(
            workspace_uuid=str(self.workspace.uuid),
            provider="qwen",
            model="qwen3.5-397b-a17b",
            prompt="Hello",
        )