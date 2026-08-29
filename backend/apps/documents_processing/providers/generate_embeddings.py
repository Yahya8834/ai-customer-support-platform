from apps.common.exceptions import EmbeddingGenerationError
from apps.common.integrations.ai_service.client import AIServiceClient


class GenerateEmbeddingsProvider:

    def __init__(self, base_url: str):
        self.client = AIServiceClient(
            base_url=base_url,
        )

    def embed(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError(
                "Cannot generate embedding for empty text"
            )

        try:
            embedding = self.client.embed(text)

            if len(embedding) != 1024:
                raise ValueError(
                    "Invalid embedding dimension"
                )

            return embedding

        except Exception as exc:
            raise EmbeddingGenerationError(
                "Failed to generate embedding"
            ) from exc

    def metadata(self) -> dict:
        return {
            "provider": "ai_service",
            "model_name": "bge-m3:567m",
        }