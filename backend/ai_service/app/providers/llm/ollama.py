from app.providers.llm.base import LLMProvider


class OllamaLLMProvider(LLMProvider):
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(self, prompt: str) -> str:
        raise NotImplementedError