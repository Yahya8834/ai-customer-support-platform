from app.providers.llm.base import LLMProvider
from app.providers.llm.ollama import OllamaLLMProvider



def test_ollama_llm_provider_implements_llm_provider():
    provider = OllamaLLMProvider(
        base_url="http://testserver",
        model="deepseek-r1",
    )

    assert isinstance(provider, LLMProvider)