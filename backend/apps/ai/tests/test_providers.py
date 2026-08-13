from unittest.mock import Mock, patch
from django.test import SimpleTestCase
from apps.ai.providers.llm.base import LLMProvider
from apps.ai.providers.llm.deepseek import DeepSeekProvider



class LLMProviderTest(SimpleTestCase):
    def test_llm_provider_requires_generate_and_stream(self):
        with self.assertRaises(TypeError):
            LLMProvider()



class DeepSeekProviderTest(SimpleTestCase):
    def test_generate_returns_response_from_client(self):
        client = Mock()
        client.chat.return_value = "The return policy is 30 days."

        provider = DeepSeekProvider(client=client)

        result = provider.generate("What is your return policy?")

        self.assertEqual(result, "The return policy is 30 days.")
        client.chat.assert_called_once_with(
            "What is your return policy?"
        )

    
    def test_deepseek_provider_requires_a_client(self):
        with self.assertRaises(TypeError):
            DeepSeekProvider()


    def test_generate_uses_client_chat_method(self):
        client = Mock()
        client.chat.return_value = "The return policy is 30 days."

        provider = DeepSeekProvider(client=client)

        result = provider.generate("What is your return policy?")

        self.assertEqual(result, "The return policy is 30 days.")
        client.chat.assert_called_once_with(
            "What is your return policy?"
        )


    def test_generate_delegates_to_client(self):
        client = Mock()
        client.chat.return_value = "The return policy is 30 days."

        provider = DeepSeekProvider(client=client)

        result = provider.generate(
            "What is your return policy?"
        )

        self.assertEqual(
            result,
            "The return policy is 30 days.",
        )

        client.chat.assert_called_once_with(
            "What is your return policy?"
        )



    def test_stream_delegates_to_client(self):
        client = Mock()
        client.stream.return_value = iter(
            ["The ", "return ", "policy ", "is 30 days."]
        )

        provider = DeepSeekProvider(client=client)

        result = list(
            provider.stream("What is your return policy?")
        )

        self.assertEqual(
            result,
            ["The ", "return ", "policy ", "is 30 days."],
        )

        client.stream.assert_called_once_with(
            "What is your return policy?"
        )



    @patch("apps.ai.providers.llm.clients.ollama.OllamaDeepSeekClient")
    def test_from_config_creates_provider(self, client_class):
        client = Mock()
        client_class.from_config.return_value = client

        provider = DeepSeekProvider.from_config(
            base_url="http://mac-host:11434",
            model="deepseek-r1",
        )

        client_class.from_config.assert_called_once_with(
            base_url="http://mac-host:11434",
            model="deepseek-r1",
        )

        self.assertIs(provider.client, client)