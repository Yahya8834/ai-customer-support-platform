import uuid
from django.db import models
from apps.documents.models import Document
from pgvector.django import VectorField



class ProcessedDocument(models.Model):

    document = models.OneToOneField(
        Document,
        on_delete=models.CASCADE,
        related_name="processed_document",
        primary_key=True,
    )

    extracted_text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )




class DocumentChunk(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    processed_document = models.ForeignKey(
        "ProcessedDocument",
        on_delete=models.CASCADE,
        related_name="chunks",
    )

    content = models.TextField()

    chunk_index = models.PositiveIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = [
            "chunk_index",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "processed_document",
                    "chunk_index",
                ],
                name="unique_document_chunk_index",
            ),
        ]



class DocumentEmbedding(models.Model):

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    chunk = models.ForeignKey(
        DocumentChunk,
        on_delete=models.CASCADE,
        related_name="embeddings",
    )

    provider = models.CharField(
        max_length=50,
    )

    model_name = models.CharField(
        max_length=100,
    )

    embedding = VectorField(
        dimensions=1024,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "chunk",
                    "provider",
                    "model_name",
                ],
                name="unique_chunk_embedding_model",
            ),
        ]

    def __str__(self):
        return (
            f"{self.provider}:{self.model_name} "
            f"→ Chunk {self.chunk.chunk_index}"
        )
    
