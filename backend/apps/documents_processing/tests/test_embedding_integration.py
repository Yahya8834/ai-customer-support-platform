import httpx
from django.test import SimpleTestCase
from apps.documents_processing.providers.generate_embeddings import (
    GenerateEmbeddingsProvider,
)


class EmbeddingIntegrationTests(SimpleTestCase):

    def test_documents_processing_can_reach_ai_service(self):
        response = httpx.post(
            "http://ai_service:8001/v1/embeddings",
            json={"text": "integration test"},
            timeout=60.0,
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.json()

        self.assertIn(
            "embedding",
            data,
        )

        self.assertEqual(
            len(data["embedding"]),
            1024,
        )



    def test_generate_embeddings_provider_works_with_real_ai_service(self):
        provider = GenerateEmbeddingsProvider(
            base_url="http://ai_service:8001",
        )

        embedding = provider.embed(
            "Apple iPhone 17 Pro Max camera specifications",
        )
        
        self.assertEqual(
            len(embedding),
            1024,
        )