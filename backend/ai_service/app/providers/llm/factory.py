from app.providers.llm.base import LLMProvider


class LLMProviderFactory:
    def __init__(self, providers: dict[str, LLMProvider]):
        self.providers = providers

    def get(self, provider_name: str) -> LLMProvider:
        try:
            return self.providers[provider_name]
        except KeyError:
            raise ValueError(
                f"Unknown LLM provider: {provider_name}"
            )