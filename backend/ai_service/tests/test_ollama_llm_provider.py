import httpx, pytest
from app.providers.llm.base import LLMProvider
from app.providers.llm.ollama import OllamaLLMProvider



def test_ollama_llm_provider_implements_llm_provider():
    provider = OllamaLLMProvider(
        base_url="http://testserver",
        model="deepseek-r1",
    )

    assert isinstance(provider, LLMProvider)




def test_ollama_llm_provider_generates_text(monkeypatch):
    def mock_post(*args, **kwargs):
        return httpx.Response(
            200,
            json={
                "message": {
                    "content": "Hello from Ollama",
                }
            },
            request=httpx.Request(
                "POST",
                "http://testserver/api/chat",
            ),
        )

    monkeypatch.setattr(httpx, "post", mock_post)

    provider = OllamaLLMProvider(
        base_url="http://testserver",
        model="deepseek-r1",
    )

    result = provider.generate("hello")

    assert result == "Hello from Ollama"



def test_ollama_llm_provider_raises_for_failed_response(monkeypatch):
    def mock_post(*args, **kwargs):
        return httpx.Response(
            500,
            request=httpx.Request(
                "POST",
                "http://testserver/api/chat",
            ),
        )

    monkeypatch.setattr(httpx, "post", mock_post)

    provider = OllamaLLMProvider(
        base_url="http://testserver",
        model="deepseek-r1",
    )

    with pytest.raises(httpx.HTTPStatusError):
        provider.generate("hello")