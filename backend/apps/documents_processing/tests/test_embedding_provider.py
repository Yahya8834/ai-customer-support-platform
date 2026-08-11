import httpx
from django.test import TestCase
from apps.common.exceptions import EmbeddingGenerationError
from apps.documents_processing.providers.generate_embeddings import (
    GenerateEmbeddingsProvider,
)
from unittest.mock import patch



class EmbeddingProviderTests(TestCase):

    def setUp(self):
        self.provider = GenerateEmbeddingsProvider(
            base_url="http://ai_service:8001",
        )

    def test_provider_returns_metadata(self):

        provider = self.provider

        metadata = provider.metadata()

        self.assertEqual(
            metadata["provider"],
            "ai_service",
        )

        self.assertEqual(
            metadata["model_name"],
            "bge-m3:567m",
        )


    def test_provider_returns_correct_embedding_dimension(self):

        provider = self.provider

        vector = provider.embed(
            "test document",
        )

        self.assertEqual(
            len(vector),
            1024,
        )



    def test_provider_rejects_empty_text(self):

            provider = self.provider

            with self.assertRaises(ValueError):
                provider.embed("")



    def test_provider_wraps_generation_errors(self):

        provider = self.provider

        provider._generate_embedding = lambda text: (
            (_ for _ in ()).throw(Exception("model failed"))
        )

        with self.assertRaises(EmbeddingGenerationError):
            provider.embed("test document")
                


    @patch("apps.documents_processing.providers.generate_embeddings.httpx.post")
    def test_provider_calls_ai_service(self, mock_post):
        mock_post.return_value.json.return_value = {
            "embedding": [0.1] * 1024,
        }
        mock_post.return_value.raise_for_status.return_value = None

        provider = self.provider

        vector = provider.embed("test document")

        mock_post.assert_called_once_with(
            "http://ai_service:8001/v1/embeddings",
            json={"text": "test document"},
            timeout=60.0,
        )

        self.assertEqual(
            vector,
            [0.1] * 1024,
        )



    @patch("apps.documents_processing.providers.generate_embeddings.httpx.post")
    def test_provider_wraps_http_errors(self, mock_post):
        mock_post.side_effect = httpx.HTTPError("AI service unavailable")

        provider = self.provider

        with self.assertRaises(EmbeddingGenerationError):
            provider.embed("test document")



    @patch("apps.documents_processing.providers.generate_embeddings.httpx.post")
    def test_provider_rejects_response_without_embedding(self, mock_post):
        mock_post.return_value.json.return_value = {
            "wrong_field": [],
        }
        mock_post.return_value.raise_for_status.return_value = None

        provider = self.provider

        with self.assertRaises(EmbeddingGenerationError):
            provider.embed("test document")


        
    @patch("apps.documents_processing.providers.generate_embeddings.httpx.post")
    def test_provider_rejects_invalid_embedding_dimension(self, mock_post):
        mock_post.return_value.json.return_value = {
            "embedding": [0.1, 0.2, 0.3],
        }
        mock_post.return_value.raise_for_status.return_value = None

        provider = self.provider

        with self.assertRaises(EmbeddingGenerationError):
            provider.embed("test document")