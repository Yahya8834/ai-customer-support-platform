from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from pathlib import Path
from apps.accounts.models import User
from apps.documents.models import Document
from apps.documents_processing.models import ProcessedDocument
from apps.workspaces.services.create_workspace import CreateWorkspaceService
from apps.documents_processing.services.process_document import ProcessDocumentService
from unittest.mock import patch




class ProcessDocumentServiceTests(TestCase):

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


    @patch(
        "apps.documents_processing.services.process_document.ProcessDocumentService._extract_text"
    )
    def test_process_document_changes_status_to_processing(
        self,
        mock_extract_text,
    ):
        mock_extract_text.side_effect = Exception("stop after processing")

        document = self.document

        with self.assertRaises(Exception):
            ProcessDocumentService.execute(
                document_uuid=document.uuid,
            )

        document.refresh_from_db()

        self.assertEqual(
            document.processing_status,
            Document.ProcessingStatus.PROCESSING,
        )

    
    def test_process_document_completes_successfully(self):

        document = ProcessDocumentService.execute(
            document_uuid=self.document.uuid,
        )

        self.assertEqual(
            document.processing_status,
            Document.ProcessingStatus.COMPLETED,
        )

    
    @patch(
        "apps.documents_processing.services.process_document.ProcessDocumentService._extract_text"
    )
    def test_process_document_stays_processing_when_pipeline_fails(
        self,
        mock_extract_text,
    ):
        mock_extract_text.side_effect = Exception(
            "extraction failed"
        )

        with self.assertRaises(Exception):
            ProcessDocumentService.execute(
                document_uuid=self.document.uuid,
            )

        self.document.refresh_from_db()

        self.assertEqual(
            self.document.processing_status,
            Document.ProcessingStatus.PROCESSING,
        )


    def test_process_document_raises_error_when_document_does_not_exist(self):
        with self.assertRaises(Document.DoesNotExist):
            ProcessDocumentService.execute(
                document_uuid="00000000-0000-0000-0000-000000000000",
            )


    @patch("apps.documents_processing.services.process_document.GetEmbeddingsService.create_embedding")
    def test_processing_same_document_twice_is_safe(self, mock_create_embedding):
        ProcessDocumentService.execute(
            document_uuid=self.document.uuid,
        )

        document = ProcessDocumentService.execute(
            document_uuid=self.document.uuid,
        )

        self.assertEqual(
            document.processing_status,
            Document.ProcessingStatus.COMPLETED,
        )

    @patch("apps.documents_processing.services.process_document.GetEmbeddingsService.create_embedding")
    def test_process_document_creates_processed_document(self, mock_create_embedding):

        ProcessDocumentService.execute(
            document_uuid=self.document.uuid,
        )

        processed_document = ProcessedDocument.objects.get(
            document=self.document,
        )

        self.assertTrue(processed_document.extracted_text)


    