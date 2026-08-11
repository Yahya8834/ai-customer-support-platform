from apps.documents_processing.models import DocumentEmbedding
from apps.documents_processing.providers.generate_embeddings import GenerateEmbeddingsProvider


class GetEmbeddingsService:

    def __init__(self, provider):
        self.provider = provider

    def create_embedding(self, chunk):

        vector = self.provider.embed(
            chunk.content,
        )

        metadata = self.provider.metadata()

        return DocumentEmbedding.objects.create(
            chunk=chunk,
            provider=metadata["provider"],
            model_name=metadata["model_name"],
            embedding=vector,
        )