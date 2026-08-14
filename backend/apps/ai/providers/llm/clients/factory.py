from .ollama import OllamaDeepSeekClient


class LLMClientFactory:
    @staticmethod
    def create(
        provider: str,
        client_type: str,
        base_url: str,
        model: str,
    ):
        if provider == "deepseek" and client_type == "ollama":
            return OllamaDeepSeekClient.from_config(
                base_url=base_url,
                model=model,
            )

        raise ValueError(
            f"Unsupported LLM client: {provider}/{client_type}"
        )