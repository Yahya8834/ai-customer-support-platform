import json
from pathlib import Path
from unittest.mock import Mock, patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from apps.documents.models import Document
from apps.documents_processing.consumers.document_uploaded_consumer import (
    on_document_uploaded,
)
from apps.workspaces.services.create_workspace import (
    CreateWorkspaceService,
)
from apps.accounts.models import User


class DocumentUploadedConsumerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="password123",
        )

        self.workspace = CreateWorkspaceService.execute(
            user=self.user,
            name="Acme Support",
        )

        fixtures_dir = Path(__file__).parent / "fixtures"
        pdf_path = fixtures_dir / "sample.pdf"

        with pdf_path.open("rb") as pdf_file:
            uploaded_pdf = SimpleUploadedFile(
                name="sample.pdf",
                content=pdf_file.read(),
                content_type="application/pdf",
            )

        self.document = Document.objects.create(
            workspace=self.workspace,
            uploaded_by=self.user,
            file=uploaded_pdf,
            original_filename=uploaded_pdf.name,
            content_type=uploaded_pdf.content_type,
            file_size=uploaded_pdf.size,
        )

        self.channel = Mock()
        self.method = Mock()
        self.method.delivery_tag = "test-delivery-tag"

    @patch(
        "apps.documents_processing.consumers.document_uploaded_consumer.ProcessDocumentService.execute"
    )
    def test_processing_failure_marks_document_as_failed(
        self,
        mock_execute,
    ):
        mock_execute.side_effect = Exception(
            "processing failed"
        )

        event = json.dumps(
            {
                "document_uuid": str(self.document.uuid),
            }
        ).encode()

        on_document_uploaded(
            self.channel,
            self.method,
            None,
            event,
        )

        self.document.refresh_from_db()

        self.assertEqual(
            self.document.processing_status,
            Document.ProcessingStatus.FAILED,
        )