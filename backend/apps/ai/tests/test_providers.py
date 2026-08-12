from django.test import SimpleTestCase
from apps.ai.providers.base import LLMProvider



class LLMProviderTest(SimpleTestCase):
    def test_llm_provider_requires_generate_and_stream(self):
        with self.assertRaises(TypeError):
            LLMProvider()