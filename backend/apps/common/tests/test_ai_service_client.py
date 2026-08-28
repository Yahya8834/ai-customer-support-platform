import httpx
from unittest.mock import patch
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