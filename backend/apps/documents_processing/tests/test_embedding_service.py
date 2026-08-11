from django.test import TestCase
from apps.workspaces.models import Workspace
from apps.documents.models import Document
from django.contrib.auth import get_user_model
from apps.documents_processing.models import (
    ProcessedDocument,
    DocumentChunk,
    DocumentEmbedding,
)
from apps.documents_processing.services.get_embeddings import GetEmbeddingsService
from apps.documents_processing.providers.generate_embeddings import GenerateEmbeddingsProvider
from django.db import IntegrityError



class FakeEmbeddingProvider:

    def embed(self, text: str):
        return [1.0] * 1024

    def metadata(self):
        return {
            "provider": "test",
            "model_name": "fake-model",
        }

class EmbeddingServiceTests(TestCase):


    def setUp(self):

        User = get_user_model()

        user = User.objects.create_user(
            username="testuser",
            password="password123",
        )

        workspace = Workspace.objects.create(
            name="Test Workspace",
        )

        document = Document.objects.create(
            workspace=workspace,
            uploaded_by=user,
            original_filename="iphone17.pdf",
            content_type="application/pdf",
            file_size=1024,
        )

        processed_document = ProcessedDocument.objects.create(
            document=document,
            extracted_text="Apple iPhone 17 Pro Max camera specifications",
        )

        self.chunk = DocumentChunk.objects.create(
            processed_document=processed_document,
            content="Apple iPhone 17 Pro Max camera specifications",
            chunk_index=0,
        )

    def test_creates_embedding_for_chunk(self):

        provider = FakeEmbeddingProvider()

        service = GetEmbeddingsService(
            provider=provider,
        )

        service.create_embedding(
            self.chunk,
        )

        self.assertEqual(
            DocumentEmbedding.objects.count(),
            1,
        )
        

    def test_cannot_create_duplicate_embedding_for_same_model(self):

        provider = FakeEmbeddingProvider()

        service = GetEmbeddingsService(
            provider=provider,
        )

        service.create_embedding(
            self.chunk,
        )

        with self.assertRaises(IntegrityError):
            service.create_embedding(self.chunk)