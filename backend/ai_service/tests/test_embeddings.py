import httpx
from  app.providers.ollama import OllamaEmbeddingProvider


def test_ollama_embedding_provider_returns_embedding(monkeypatch):
    def mock_post(*args, **kwargs):
        return httpx.Response(
            200,
            json={
                "embeddings": [
                    [0.1, 0.2, 0.3],
                ]
            },
            request=httpx.Request(
                "POST",
                "http://testserver/api/embed",
            ),
        )

    monkeypatch.setattr(httpx, "post", mock_post)

    provider = OllamaEmbeddingProvider(
        base_url="http://testserver",
        model="bge-m3:567m",
    )

    result = provider.generate("hello")

    assert result == [0.1, 0.2, 0.3]


