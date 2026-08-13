import httpx
import json
from .deepseek import DeepSeekClient


class OllamaDeepSeekClient(DeepSeekClient):
    def __init__(
        self,
        ollama,
        base_url: str | None = None,
        model: str | None = None,
    ):
        self.ollama = ollama
        self.base_url = base_url
        self.model = model

    @classmethod
    def from_config(cls, base_url: str, model: str):
        client = httpx.Client(
            base_url=base_url,
        )

        return cls(
            ollama=client,
            base_url=base_url,
            model=model,
        )

    def chat(self, prompt: str) -> str:
        response = self.ollama.post(
            "/api/chat",
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
        )

        return response.json()["message"]["content"]


    def stream(self, prompt: str):
        response = self.ollama.post(
            "/api/chat",
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                "stream": True,
            },
        )

        for line in response.iter_lines():
            if not line:
                continue

            chunk = json.loads(line)
            content = chunk.get("message", {}).get("content")

            if content:
                yield content