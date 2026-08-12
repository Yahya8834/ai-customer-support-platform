from django.test import SimpleTestCase
from apps.ai.providers.base import LLMProvider
from unittest.mock import Mock



class LLMProviderTest(SimpleTestCase):
    def test_llm_provider_requires_generate_and_stream(self):
        with self.assertRaises(TypeError):
            LLMProvider()



class DeepSeekProviderTest(SimpleTestCase):
    def test_generate_returns_response_from_client(self):
        client = Mock()
        client.generate.return_value = "The return policy is 30 days."

        provider = DeepSeekProvider(client=client)

        result = provider.generate("What is your return policy?")

        self.assertEqual(result, "The return policy is 30 days.")
        client.generate.assert_called_once_with(
            "What is your return policy?"
        )