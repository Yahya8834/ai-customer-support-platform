from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.workspaces.models import Workspace
from apps.documents.models import Document
from apps.documents_processing.models import (
    DocumentChunk,
    DocumentEmbedding,
)
from apps.documents_processing.services.process_document import (
    ProcessDocumentService,
)
from django.core.files import File
from pathlib import Path



class EmbeddingPipelineTests(TestCase):

    @patch("apps.documents_processing.services.process_document.PdfTextExtractionService.execute")
    def test_processing_document_creates_embeddings(self,mock_extract_text,):

        User = get_user_model()

        user = User.objects.create_user(
            username="pipeline-user",
            password="password123",
        )

        workspace = Workspace.objects.create(
            name="Pipeline Workspace",
        )

        fixture_path = (
            Path(__file__).resolve().parent
            / "fixtures"
            / "sample.pdf"
        )

        with fixture_path.open("rb") as pdf:
            document = Document.objects.create(
                workspace=workspace,
                uploaded_by=user,
                file=File(pdf, name="sample.pdf"),
                original_filename="sample.pdf",
                content_type="application/pdf",
                file_size=fixture_path.stat().st_size,
            )

        mock_extract_text.return_value = (
            "Apple iPhone 17 Pro Max camera specifications"
        )

        ProcessDocumentService.execute(
            document_uuid=document.uuid,
        )

        self.assertGreater(
            DocumentChunk.objects.count(),
            0,
        )

        self.assertEqual(
            DocumentEmbedding.objects.count(),
            DocumentChunk.objects.count(),
        )