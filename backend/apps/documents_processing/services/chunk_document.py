from apps.documents_processing.models import (
    DocumentChunk,
    ProcessedDocument,
)
from apps.documents_processing.services.text_splitter import (
    RecursiveTextSplitter,
)



class ChunkDocumentService:

    @staticmethod
    def execute(*, document_uuid):

        processed_document = ProcessedDocument.objects.get(
            document__uuid=document_uuid,
        )

        if not processed_document.extracted_text.strip():
            return processed_document

        splitter = RecursiveTextSplitter()

        chunks = splitter.split_text(
            processed_document.extracted_text,
        )

        DocumentChunk.objects.filter(
            processed_document=processed_document,
        ).delete()

        document_chunks = []

        for index, chunk in enumerate(chunks):

            document_chunks.append(
                DocumentChunk(
                    processed_document=processed_document,
                    content=chunk,
                    chunk_index=index,
                )
            )

        DocumentChunk.objects.bulk_create(
            document_chunks,
        )

        return processed_document