import httpx
from unittest.mock import patch, MagicMock
from django.test import TestCase
from apps.common.integrations.ai_service.client import AIServiceClient
from apps.common.exceptions import AIServiceError



class AIServiceClientTests(TestCase):

    @patch("apps.common.integrations.ai_service.client.httpx.post")
    def test_embed_sends_text_to_ai_service(self, mock_post):
        mock_post.return_value.json.return_value = {
            "embedding": [0.1] * 1024,
        }
        mock_post.return_value.raise_for_status.return_value = None

        client = AIServiceClient(
            base_url="http://ai_service:8001",
        )

        result = client.embed("test document")

        mock_post.assert_called_once_with(
            "http://ai_service:8001/v1/embeddings",
            json={"text": "test document"},
            timeout=60.0,
        )

        self.assertEqual(
            result,
            [0.1] * 1024,
        )


    
    @patch("apps.common.integrations.ai_service.client.httpx.post")
    def test_embed_raises_ai_service_error_when_response_has_no_embedding(
        self,
        mock_post,
    ):
        mock_post.return_value.json.return_value = {
            "wrong_field": [],
        }
        mock_post.return_value.raise_for_status.return_value = None

        client = AIServiceClient(
            base_url="http://ai_service:8001",
        )

        with self.assertRaises(AIServiceError):
            client.embed("test document")


    
    @patch("apps.common.integrations.ai_service.client.httpx.post")
    def test_embed_raises_ai_service_error_when_http_fails(
        self,
        mock_post,
    ):
        mock_post.side_effect = httpx.HTTPError(
            "AI service unavailable"
        )

        client = AIServiceClient(
            base_url="http://ai_service:8001",
        )

        with self.assertRaises(AIServiceError):
            client.embed("test document")


    @patch("apps.common.integrations.ai_service.client.httpx.post")
    def test_embed_raises_ai_service_error_for_invalid_embedding_dimension(
        self,
        mock_post,
    ):
        mock_post.return_value.json.return_value = {
            "embedding": [0.1, 0.2, 0.3],
        }
        mock_post.return_value.raise_for_status.return_value = None

        client = AIServiceClient(
            base_url="http://ai_service:8001",
        )

        result = client.embed("test document")

        self.assertEqual(
            result,
            [0.1, 0.2, 0.3],
        )


    @patch("apps.common.integrations.ai_service.client.httpx.post")
    def test_chat_calls_ai_service(self, mock_post):
            mock_post.return_value.json.return_value = {
                "response": "Hello from AI service",
            }
            mock_post.return_value.raise_for_status.return_value = None

            client = AIServiceClient(
                base_url="http://ai_service:8001",
            )

            result = client.chat(
                workspace_uuid="550e8400-e29b-41d4-a716-446655440000",
                provider="ollama",
                model="deepseek-r1:8b",
                prompt="Hello",
            )

            mock_post.assert_called_once_with(
                "http://ai_service:8001/v1/chat",
                json={
                    "workspace_uuid": "550e8400-e29b-41d4-a716-446655440000",
                    "provider": "ollama",
                    "model": "deepseek-r1:8b",
                    "prompt": "Hello",
                },
                timeout=60.0,
            )

            self.assertEqual(
                result,
                "Hello from AI service",
            )


    @patch("apps.common.integrations.ai_service.client.httpx.post")
    def test_chat_raises_ai_service_error_on_failure(self, mock_post):
        mock_post.side_effect = httpx.HTTPError(
            "AI service unavailable"
        )

        client = AIServiceClient(
            base_url="http://ai_service:8001",
        )

        with self.assertRaises(AIServiceError):
            client.chat(
                workspace_uuid="550e8400-e29b-41d4-a716-446655440000",
                provider="ollama",
                model="deepseek-r1:8b",
                prompt="Hello",
            )


    @patch("apps.common.integrations.ai_service.client.httpx.post")
    def test_chat_raises_ai_service_error_when_response_has_no_response(
        self,
        mock_post,
    ):
        mock_post.return_value.json.return_value = {
            "wrong_field": "Hello",
        }
        mock_post.return_value.raise_for_status.return_value = None

        client = AIServiceClient(
            base_url="http://ai_service:8001",
        )

        with self.assertRaises(AIServiceError):
            client.chat(
                workspace_uuid="550e8400-e29b-41d4-a716-446655440000",
                provider="ollama",
                model="deepseek-r1:8b",
                prompt="Hello",
            )


    
    @patch("apps.common.integrations.ai_service.client.httpx.stream")
    def test_chat_stream_calls_ai_service(self, mock_stream):

        mock_response = MagicMock()
        mock_response.__enter__.return_value = mock_response
        mock_response.iter_text.return_value = [
            "Hello",
            " from",
            " Qwen",
        ]

        mock_stream.return_value = mock_response

        client = AIServiceClient(
            base_url="http://ai_service:8001",
        )

        result = list(
            client.chat_stream(
                workspace_uuid="550e8400-e29b-41d4-a716-446655440000",
                provider="qwen",
                model="qwen3.5-397b-a17b",
                prompt="Hello",
            )
        )

        mock_stream.assert_called_once_with(
            "POST",
            "http://ai_service:8001/v1/chat/stream",
            json={
                "workspace_uuid": "550e8400-e29b-41d4-a716-446655440000",
                "provider": "qwen",
                "model": "qwen3.5-397b-a17b",
                "prompt": "Hello",
            },
            timeout=120.0,
        )

        self.assertEqual(
            result,
            ["Hello", " from", " Qwen"],
        )


    @patch("apps.common.integrations.ai_service.client.httpx.stream")
    def test_chat_stream_ignores_empty_chunks(self, mock_stream):

        mock_response = MagicMock()
        mock_response.__enter__.return_value = mock_response
        mock_response.iter_text.return_value = [
            "Hello",
            "",
            " world",
            "",
        ]

        mock_stream.return_value = mock_response

        client = AIServiceClient(
            base_url="http://ai_service:8001",
        )

        result = list(
            client.chat_stream(
                workspace_uuid="550e8400-e29b-41d4-a716-446655440000",
                provider="qwen",
                model="qwen3.5-397b-a17b",
                prompt="Hello",
            )
        )

        self.assertEqual(
            result,
            ["Hello", " world"],
        )


    @patch("apps.common.integrations.ai_service.client.httpx.stream")
    def test_chat_stream_raises_ai_service_error_on_http_failure(
        self,
        mock_stream,
    ):
        mock_stream.side_effect = httpx.HTTPError(
            "AI service unavailable"
        )

        client = AIServiceClient(
            base_url="http://ai_service:8001",
        )

        with self.assertRaises(AIServiceError):
            list(
                client.chat_stream(
                    workspace_uuid="550e8400-e29b-41d4-a716-446655440000",
                    provider="qwen",
                    model="qwen3.5-397b-a17b",
                    prompt="Hello",
                )
            )