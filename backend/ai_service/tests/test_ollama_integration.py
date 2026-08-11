import os
from app.providers.ollama import OllamaEmbeddingProvider
import httpx
import pytest


@pytest.mark.integration
def test_ollama_bge_m3_returns_embedding():
    base_url = os.environ["BGE_API_URL"]
    model = os.environ["BGE_MODEL"]

    response = httpx.post(
        f"{base_url}/api/embed",
        json={
            "model": model,
            "input": "hello world",
        },
        timeout=60.0,
    )

    response.raise_for_status()

    data = response.json()

    assert "embeddings" in data
    assert len(data["embeddings"]) == 1
    assert len(data["embeddings"][0]) > 0



@pytest.mark.integration
def test_ollama_embedding_provider_works_with_real_service():
    base_url = os.environ["BGE_API_URL"]
    model = os.environ["BGE_MODEL"]

    provider = OllamaEmbeddingProvider(
        base_url=base_url,
        model=model,
    )

    embedding = provider.generate("hello world")

    assert isinstance(embedding, list)
    assert len(embedding) > 0
    assert all(isinstance(value, float) for value in embedding)



@pytest.mark.integration
def test_ollama_embedding_provider_works_with_real_service():
    base_url = os.environ["BGE_API_URL"]
    model = os.environ["BGE_MODEL"]

    provider = OllamaEmbeddingProvider(
        base_url=base_url,
        model=model,
    )

    embedding = provider.generate("hello world")


    assert isinstance(embedding, list)
    assert len(embedding) > 0
    assert all(isinstance(value, float) for value in embedding)