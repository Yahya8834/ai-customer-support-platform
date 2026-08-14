from collections.abc import Iterator
from .base import LLMProvider
from apps.ai.providers.llm.clients.factory import LLMClientFactory


class DeepSeekProvider(LLMProvider):
    def __init__(self, client):
        self.client = client

    def generate(self, prompt: str) -> str:
        return self.client.chat(prompt)

    def stream(self, prompt: str) -> Iterator[str]:
        return self.client.stream(prompt)
    
    
    @classmethod
    def from_config(
        cls,
        base_url: str,
        model: str,
        client_type: str = "ollama",
    ):
        client = LLMClientFactory.create(
            provider="deepseek",
            client_type=client_type,
            base_url=base_url,
            model=model,
        )

        return cls(client=client)