import httpx
from app.providers.llm.base import LLMProvider


class OllamaLLMProvider(LLMProvider):
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(self, prompt: str) -> str:
        response = httpx.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                "stream": False,
            },
            timeout=60.0,
        )

        response.raise_for_status()

        return response.json()["message"]["content"]