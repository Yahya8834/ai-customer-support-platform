import httpx
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
        response = self.ollama.chat(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt},
            ],
        )

        return response["message"]["content"]

    def stream(self, prompt: str):
        for chunk in self.ollama.chat(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt},
            ],
            stream=True,
        ):
            yield chunk["message"]["content"]