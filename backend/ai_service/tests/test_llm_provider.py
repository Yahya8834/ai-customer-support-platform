import pytest
from app.providers.llm.base import LLMProvider



def test_llm_provider_requires_generate():
    with pytest.raises(TypeError):
        LLMProvider()