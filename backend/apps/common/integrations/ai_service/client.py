import httpx
from collections.abc import Iterator
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
    
    
    def chat(
        self,
        *,
        workspace_uuid: str,
        provider: str,
        model: str,
        prompt: str,
    ) -> str:
        try:
            response = httpx.post(
                f"{self.base_url}/v1/chat",
                json={
                    "workspace_uuid": workspace_uuid,
                    "provider": provider,
                    "model": model,
                    "prompt": prompt,
                },
                timeout=60.0,
            )

            response.raise_for_status()

            return response.json()["response"]

        except (httpx.HTTPError, KeyError, TypeError, ValueError) as exc:
            raise AIServiceError(
                "Failed to generate response through AI service."
            ) from exc
        

    def chat_stream(
        self,
        *,
        workspace_uuid: str,
        provider: str,
        model: str,
        prompt: str,
    ) -> Iterator[str]:
        try:
            with httpx.stream(
                "POST",
                f"{self.base_url}/v1/chat/stream",
                json={
                    "workspace_uuid": workspace_uuid,
                    "provider": provider,
                    "model": model,
                    "prompt": prompt,
                },
                timeout=120.0,
            ) as response:
                response.raise_for_status()

                for chunk in response.iter_text():
                    if chunk:
                        yield chunk

        except (httpx.HTTPError, ValueError) as exc:
            raise AIServiceError(
                "Failed to stream response from AI service."
            ) from exc