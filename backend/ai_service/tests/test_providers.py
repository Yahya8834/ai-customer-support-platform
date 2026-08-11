from app.providers.base import EmbeddingProvider
from app.providers.ollama import OllamaEmbeddingProvider


def test_ollama_provider_implements_embedding_provider():
    provider = OllamaEmbeddingProvider(
        base_url="http://testserver",
        model="bge-m3:567m",
    )

    assert isinstance(provider, EmbeddingProvider)