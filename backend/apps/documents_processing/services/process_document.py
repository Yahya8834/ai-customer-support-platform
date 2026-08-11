from apps.documents.models import Document
from apps.documents_processing.models import ProcessedDocument, DocumentChunk
from apps.documents_processing.services.extract_pdf_text import (
    PdfTextExtractionService,
)
from apps.documents_processing.services.chunk_document import (
    ChunkDocumentService,
)
from django.conf import settings

from apps.documents_processing.providers.generate_embeddings import (
    GenerateEmbeddingsProvider,
)
from apps.documents_processing.services.get_embeddings import (
    GetEmbeddingsService,
)



class ProcessDocumentService:

    @staticmethod
    def execute(*, document_uuid):
        document = Document.objects.get(
            uuid=document_uuid,
        )

        ProcessDocumentService._mark_processing(
            document=document,
        )

        extracted_text = ProcessDocumentService._extract_text(
            document=document,
        )

        ProcessDocumentService._create_processed_document(
            document=document,
            extracted_text=extracted_text,
        )

        ChunkDocumentService.execute(
            document_uuid=document_uuid,
        )

        provider = GenerateEmbeddingsProvider(
            base_url=settings.AI_SERVICE_URL,
        )

        embedding_service = GetEmbeddingsService(
            provider=provider,
        )

        chunks = DocumentChunk.objects.filter(
            processed_document__document__uuid=document_uuid,
        )

        for chunk in chunks:
            embedding_service.create_embedding(
                chunk,
            )


        document.processing_status = (
            Document.ProcessingStatus.COMPLETED
        )

        document.save(
            update_fields=[
                "processing_status",
            ]
        )

        return document

    @staticmethod
    def _mark_processing(*, document):
        document.processing_status = (
            Document.ProcessingStatus.PROCESSING
        )

        document.save(
            update_fields=[
                "processing_status",
            ]
        )

    @staticmethod
    def _extract_text(*, document):
        return PdfTextExtractionService.execute(
            document.file.path,
        )

    @staticmethod
    def _create_processed_document(
        *,
        document,
        extracted_text,
    ):
        ProcessedDocument.objects.get_or_create(
            document=document,
            defaults={
                "extracted_text": extracted_text,
            },
        )