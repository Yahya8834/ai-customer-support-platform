import httpx

from apps.common.exceptions import AIServiceError


class AIServiceClient:

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def embed(self, text: str) -> list[float]:
        try:
            response = httpx.post(
                f"{self.base_url}/v1/embeddings",
                json={"text": text},
                timeout=60.0,
            )

            response.raise_for_status()

            embedding = response.json()["embedding"]

        except (httpx.HTTPError, KeyError, TypeError, ValueError) as exc:
            raise AIServiceError(
                "Failed to generate embedding through AI service."
            ) from exc

        return embedding
    
