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



    @patch("apps.documents_processing.providers.generate_embeddings.AIServiceClient")
    def test_provider_wraps_generation_errors(self, mock_client):
        mock_client.return_value.embed.side_effect = Exception(
            "model failed"
        )

        provider = GenerateEmbeddingsProvider(
            base_url="http://ai_service:8001",
        )

        with self.assertRaises(EmbeddingGenerationError):
            provider.embed("test document")
                    


    @patch(
        "apps.documents_processing.providers.generate_embeddings.AIServiceClient"
    )
    def test_provider_rejects_invalid_embedding_dimension(
        self,
        mock_client,
    ):
        mock_client.return_value.embed.return_value = [
            0.1,
            0.2,
            0.3,
        ]

        provider = GenerateEmbeddingsProvider(
            base_url="http://ai_service:8001",
        )

        with self.assertRaises(EmbeddingGenerationError):
            provider.embed("test document")


    @patch(
        "apps.documents_processing.providers.generate_embeddings.AIServiceClient"
    )
    def test_provider_uses_ai_service_client(self, mock_client):
        mock_client.return_value.embed.return_value = [0.1] * 1024

        provider = GenerateEmbeddingsProvider(
            base_url="http://ai_service:8001",
        )

        result = provider.embed("test document")

        mock_client.assert_called_once_with(
            base_url="http://ai_service:8001",
        )

        mock_client.return_value.embed.assert_called_once_with(
            "test document",
        )

        self.assertEqual(
            result,
            [0.1] * 1024,
        )