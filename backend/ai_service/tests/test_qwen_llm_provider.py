import pytest
from unittest.mock import Mock
from app.providers.llm.qwen import QwenLLMProvider
from app.providers.llm.base import LLMProvider


def test_qwen_llm_provider_generates_text():
    client = Mock()

    client.chat.completions.create.return_value = Mock(
        choices=[
            Mock(
                message=Mock(
                    content="Hello from Qwen",
                ),
            ),
        ],
    )

    provider = QwenLLMProvider(
        api_key="test-key",
    )

    provider.client = client

    result = provider.generate(
        "hello",
        "qwen3.5-397b-a17b",
    )

    assert result == "Hello from Qwen"



def test_qwen_llm_provider_rejects_empty_prompt():
    provider = QwenLLMProvider(
        api_key="test-key",
    )

    with pytest.raises(ValueError, match="prompt cannot be empty"):
        provider.generate(
            "   ",
            "qwen3.5-397b-a17b",
        )


def test_qwen_llm_provider_sends_model_and_prompt():
    client = Mock()

    client.chat.completions.create.return_value = Mock(
        choices=[
            Mock(
                message=Mock(
                    content="response",
                ),
            ),
        ],
    )

    provider = QwenLLMProvider(
        api_key="test-key",
    )

    provider.client = client

    result = provider.generate(
        "hello",
        "qwen3.5-397b-a17b",
    )

    assert result == "response"

    client.chat.completions.create.assert_called_once_with(
        model="qwen3.5-397b-a17b",
        messages=[
            {
                "role": "user",
                "content": "hello",
            },
        ],
    )



def test_qwen_llm_provider_requires_message_content():
    client = Mock()

    client.chat.completions.create.return_value = Mock(
        choices=[
            Mock(
                message=Mock(
                    content=None,
                ),
            ),
        ],
    )

    provider = QwenLLMProvider(
        api_key="test-key",
    )

    provider.client = client

    with pytest.raises(ValueError, match="response content is missing"):
        provider.generate(
            "hello",
            "qwen3.5-397b-a17b",
        )





def test_qwen_llm_provider_implements_llm_provider():
    provider = QwenLLMProvider(
        api_key="test-key",
    )

    assert isinstance(provider, LLMProvider)