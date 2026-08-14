from unittest.mock import Mock, patch
from django.test import SimpleTestCase
from apps.ai.providers.llm.clients.factory import LLMClientFactory


class LLMClientFactoryTest(SimpleTestCase):
    @patch(
        "apps.ai.providers.llm.clients.factory.OllamaDeepSeekClient"
    )
    def test_creates_ollama_deepseek_client(self, client_class):
        client = Mock()
        client_class.from_config.return_value = client

        result = LLMClientFactory.create(
            provider="deepseek",
            client_type="ollama",
            base_url="http://mac-host:11434",
            model="deepseek-r1",
        )

        client_class.from_config.assert_called_once_with(
            base_url="http://mac-host:11434",
            model="deepseek-r1",
        )

        self.assertIs(result, client)



    def test_rejects_unsupported_client(self):
        with self.assertRaises(ValueError):
            LLMClientFactory.create(
                provider="deepseek",
                client_type="unsupported",
                base_url="http://mac-host:11434",
                model="deepseek-r1",
            )

    

    def test_rejects_unsupported_provider(self):
        with self.assertRaises(ValueError):
            LLMClientFactory.create(
                provider="unsupported",
                client_type="ollama",
                base_url="http://mac-host:11434",
                model="deepseek-r1",
            )

    

    def test_requires_client_type(self):
        with self.assertRaises(TypeError):
            LLMClientFactory.create(
                provider="deepseek",
                base_url="http://mac-host:11434",
                model="deepseek-r1",
            )