from apps.documents_processing.models import DocumentEmbedding
from pgvector.django import CosineDistance


class VectorSearch:

    def search(
        self,
        *,
        workspace_uuid: str,
        embedding: list[float],
    ):
        return self._query_database(
            workspace_uuid=workspace_uuid,
            embedding=embedding,
        )

    def _query_database(
        self,
        *,
        workspace_uuid: str,
        embedding: list[float],
    ):
        embeddings = (
            DocumentEmbedding.objects
            .filter(
                chunk__processed_document__document__workspace__uuid=workspace_uuid,
            )
            .annotate(
                distance=CosineDistance(
                    "embedding",
                    embedding,
                ),
            )
            .order_by("distance")
        )

        return [
            embedding.chunk
            for embedding in embeddings
        ]