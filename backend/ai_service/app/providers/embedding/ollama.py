import httpx
from app.providers.embedding.base import EmbeddingProvider


class OllamaEmbeddingProvider(EmbeddingProvider):
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def embed(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError("text cannot be empty")

        response = httpx.post(
            f"{self.base_url}/api/embeddings",
            json={
                "model": self.model,
                "prompt": text,
            },
            timeout=120.0,
        )

        response.raise_for_status()

        return response.json()["embedding"]