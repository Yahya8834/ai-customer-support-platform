from django.contrib import admin

from apps.documents_processing.models import (
    ProcessedDocument,
    DocumentChunk,
    DocumentEmbedding,
)


@admin.register(ProcessedDocument)
class ProcessedDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "document",
        "created_at",
        "updated_at",
    )


@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "processed_document",
        "chunk_index",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "uuid",
        "content",
    )


@admin.register(DocumentEmbedding)
class DocumentEmbeddingAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "chunk",
        "provider",
        "model_name",
        "created_at",
    )

    list_filter = (
        "provider",
        "model_name",
        "created_at",
    )

    search_fields = (
        "uuid",
        "provider",
        "model_name",
    )