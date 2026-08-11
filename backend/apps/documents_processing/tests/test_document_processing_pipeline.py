from pathlib import Path
from django.test import TestCase
from apps.accounts.models import User
from apps.documents.models import Document
from apps.documents_processing.models import (
    ProcessedDocument,
    DocumentChunk,
)
from apps.documents_processing.services.process_document import (
    ProcessDocumentService,
)
from apps.workspaces.services.create_workspace import (
    CreateWorkspaceService,
)
from django.core.files import File




class DocumentProcessingPipelineTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="password123",
        )

        self.workspace = CreateWorkspaceService.execute(
            user=self.user,
            name="Apple Support",
        )

        fixture_path = (
            Path(__file__).parent
            / "fixtures"
            / "sample.pdf"
        )

        with fixture_path.open("rb") as pdf_file:
            django_file = File(
                pdf_file,
                name="sample.pdf",
            )

            self.document = Document.objects.create(
                workspace=self.workspace,
                uploaded_by=self.user,
                file=django_file,
                original_filename="sample.pdf",
                content_type="application/pdf",
                file_size=fixture_path.stat().st_size,
            )


    def test_document_is_extracted_and_chunked(self):

        ProcessDocumentService.execute(
            document_uuid=self.document.uuid,
        )

        processed_document = ProcessedDocument.objects.get(
            document=self.document,
        )

        self.assertTrue(
            processed_document.extracted_text,
        )


        chunks = DocumentChunk.objects.filter(
            processed_document=processed_document,
        )

        self.assertGreater(
            chunks.count(),
            0,
        )

