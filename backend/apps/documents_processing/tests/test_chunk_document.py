from django.test import TestCase

from apps.accounts.models import User
from apps.documents.models import Document
from apps.documents_processing.models import (
    ProcessedDocument,
    DocumentChunk,
)
from apps.documents_processing.services.chunk_document import (
    ChunkDocumentService,
)
from apps.workspaces.services.create_workspace import (
    CreateWorkspaceService,
)


class ChunkDocumentServiceTests(TestCase):

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

        self.document = Document.objects.create(
            workspace=self.workspace,
            uploaded_by=self.user,
            original_filename="manual.pdf",
            content_type="application/pdf",
            file_size=1000,
        )

        self.processed_document = ProcessedDocument.objects.create(
            document=self.document,
            extracted_text=(
                "This is the first paragraph. "
                "This is the second paragraph. "
                "This is the third paragraph."
            ),
        )

    def test_creates_document_chunks(self):
        ChunkDocumentService.execute(
            document_uuid=self.document.uuid,
        )

        chunks = DocumentChunk.objects.filter(
            processed_document=self.processed_document,
        )

        self.assertGreater(
            chunks.count(),
            0,
        )

        self.assertEqual(
            chunks.first().chunk_index,
            0,
        )


    def test_empty_text_does_not_create_chunks(self):
        self.processed_document.extracted_text = ""
        self.processed_document.save()

        ChunkDocumentService.execute(
            document_uuid=self.document.uuid,
        )

        chunks = DocumentChunk.objects.filter(
            processed_document=self.processed_document,
        )

        self.assertEqual(
            chunks.count(),
            0,
        )


    def test_processing_document_twice_does_not_duplicate_chunks(self):
        ChunkDocumentService.execute(
            document_uuid=self.document.uuid,
        )

        first_count = DocumentChunk.objects.filter(
            processed_document=self.processed_document,
        ).count()

        ChunkDocumentService.execute(
            document_uuid=self.document.uuid,
        )

        second_count = DocumentChunk.objects.filter(
            processed_document=self.processed_document,
        ).count()

        self.assertEqual(
            first_count,
            second_count,
        )


    def test_chunks_are_created_in_order(self):
        ChunkDocumentService.execute(
            document_uuid=self.document.uuid,
        )

        chunks = DocumentChunk.objects.filter(
            processed_document=self.processed_document,
        )

        indexes = list(
            chunks.values_list(
                "chunk_index",
                flat=True,
            )
        )

        self.assertEqual(
            indexes,
            sorted(indexes),
        )


        