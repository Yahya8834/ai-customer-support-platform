import httpx
from apps.common.exceptions import EmbeddingGenerationError



class GenerateEmbeddingsProvider:

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def embed(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError(
                "Cannot generate embedding for empty text"
            )

        try:
            return self._generate_embedding(text)

        except Exception as exc:
            raise EmbeddingGenerationError(
                "Failed to generate embedding"
            ) from exc
        

    def _generate_embedding(self, text: str) -> list[float]:
        response = httpx.post(
            f"{self.base_url}/v1/embeddings",
            json={"text": text},
            timeout=60.0,
        )

        response.raise_for_status()

        embedding = response.json()["embedding"]

        if len(embedding) != 1024:
            raise ValueError(
                "Invalid embedding dimension"
            )

        return embedding
    

    def metadata(self) -> dict:
        return {
            "provider": "ai_service",
            "model_name": "bge-m3:567m",
        }