from unittest.mock import MagicMock
from app.providers.embedding.base import EmbeddingProvider
from app.providers.embedding.ollama import OllamaEmbeddingProvider
from app.providers.llm.qwen import QwenLLMProvider


def test_ollama_provider_implements_embedding_provider():
    provider = OllamaEmbeddingProvider(
        base_url="http://testserver",
        model="bge-m3:567m",
    )

    assert isinstance(provider, EmbeddingProvider)



def test_qwen_provider_streams_response():
    client = MagicMock()

    chunks = [
        MagicMock(
            choices=[
                MagicMock(
                    delta=MagicMock(content="Hello"),
                )
            ]
        ),
        MagicMock(
            choices=[
                MagicMock(
                    delta=MagicMock(content=" world"),
                )
            ]
        ),
        MagicMock(choices=[]),
    ]

    client.chat.completions.create.return_value = iter(chunks)

    provider = QwenLLMProvider(api_key="test-key")
    provider.client = client

    result = list(
        provider.stream(
            prompt="hello",
            model="qwen3.5-397b-a17b",
        )
    )

    assert result == ["Hello", " world"]

    client.chat.completions.create.assert_called_once_with(
        model="qwen3.5-397b-a17b",
        messages=[
            {
                "role": "user",
                "content": "hello",
            },
        ],
        stream=True,
    )