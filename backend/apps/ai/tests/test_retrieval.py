from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import Mock
from apps.workspaces.models import Workspace
from apps.documents.models import Document
from apps.documents_processing.models import (
    ProcessedDocument,
    DocumentChunk,
    DocumentEmbedding,
)
from apps.ai.retrieval.vector_search import VectorSearch



class VectorSearchTests(TestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
        )

        self.workspace = Workspace.objects.create(
            name="Test Workspace",
            slug="test-workspace",
        )

        document = Document.objects.create(
            workspace=self.workspace,
            uploaded_by=self.user,
            original_filename="guide.pdf",
            content_type="application/pdf",
            file_size=1024,
        )

        processed_document = ProcessedDocument.objects.create(
            document=document,
            extracted_text="Password reset instructions",
        )

        self.chunk = DocumentChunk.objects.create(
            processed_document=processed_document,
            content="Password reset instructions",
            chunk_index=0,
        )

        self.embedding = [1.0] * 1024

        DocumentEmbedding.objects.create(
            chunk=self.chunk,
            provider="test",
            model_name="fake-model",
            embedding=self.embedding,
        )


    def test_vector_search_returns_relevant_chunks(self):
        embedding = [0.1] * 1024

        chunk = Mock()
        chunk.content = "Password reset instructions"

        search = VectorSearch()

        search._query_database = Mock(
            return_value=[chunk],
        )

        results = search.search(
            workspace_uuid="550e8400-e29b-41d4-a716-446655440000",
            embedding=embedding,
        )

        self.assertEqual(
            results,
            [chunk],
        )


    def test_search_passes_workspace_and_embedding_to_database_query(self):
        embedding = [0.1] * 1024

        search = VectorSearch()

        search._query_database = Mock(
            return_value=[],
        )

        search.search(
            workspace_uuid="550e8400-e29b-41d4-a716-446655440000",
            embedding=embedding,
        )

        search._query_database.assert_called_once_with(
            workspace_uuid="550e8400-e29b-41d4-a716-446655440000",
            embedding=embedding,
            top_k=5
        )


    def test_search_returns_chunks_from_workspace(self):
        search = VectorSearch()

        results = search.search(
            workspace_uuid=str(self.workspace.uuid),
            embedding=self.embedding,
        )

        self.assertEqual(
            len(results),
            1,
        )

        self.assertEqual(
            results[0].content,
            "Password reset instructions",
        )


    def test_search_limits_results_to_top_k(self):
        search = VectorSearch()

        results = search.search(
            workspace_uuid=str(self.workspace.uuid),
            embedding=self.embedding,
            top_k=1,
        )

        self.assertEqual(
            len(results),
            1,
        )