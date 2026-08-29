import httpx, pytest
from app.providers.llm.base import LLMProvider
from app.providers.llm.ollama import OllamaLLMProvider



def test_ollama_llm_provider_implements_llm_provider():
    provider = OllamaLLMProvider(
        base_url="http://testserver",
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
    )

    result = provider.generate("hello", "deepseek-r1:8b")

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
    )

    with pytest.raises(httpx.HTTPStatusError):
        provider.generate("hello", "deepseek-r1:8b")



def test_ollama_llm_provider_requires_message_content(monkeypatch):
    def mock_post(*args, **kwargs):
        return httpx.Response(
            200,
            json={
                "message": {},
            },
            request=httpx.Request(
                "POST",
                "http://testserver/api/chat",
            ),
        )

    monkeypatch.setattr(httpx, "post", mock_post)

    provider = OllamaLLMProvider(
        base_url="http://testserver",
    )

    with pytest.raises(KeyError):
        provider.generate("hello", "deepseek-r1:8b")



def test_ollama_llm_provider_rejects_empty_prompt():
    provider = OllamaLLMProvider(
        base_url="http://testserver",
    )

    with pytest.raises(ValueError, match="prompt cannot be empty"):
        provider.generate("   ", "deepseek-r1:8b")



def test_ollama_llm_provider_sends_model_and_prompt(monkeypatch):
    captured = {}

    def mock_post(*args, **kwargs):
        captured["url"] = args[0]
        captured["json"] = kwargs["json"]

        return httpx.Response(
            200,
            json={
                "message": {
                    "content": "response",
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
    )

    result = provider.generate("hello", "deepseek-r1:8b")

    assert result == "response"
    assert captured["url"] == "http://testserver/api/chat"
    assert captured["json"] == {
        "model": "deepseek-r1:8b",
        "messages": [
            {
                "role": "user",
                "content": "hello",
            },
        ],
        "stream": False,
    }