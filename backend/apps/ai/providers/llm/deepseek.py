from collections.abc import Iterator

from .base import LLMProvider


class DeepSeekProvider(LLMProvider):
    def __init__(self, client):
        self.client = client

    def generate(self, prompt: str) -> str:
        return self.client.generate(prompt)

    def stream(self, prompt: str) -> Iterator[str]:
        return self.client.stream(prompt)