from django.test import SimpleTestCase
from apps.ai.providers.llm.clients.deepseek import DeepSeekClient
from unittest.mock import Mock, patch
from apps.ai.providers.llm.clients.ollama import OllamaDeepSeekClient


class DeepSeekClientTest(SimpleTestCase):
    def test_client_requires_chat_and_stream(self):
        with self.assertRaises(TypeError):
            DeepSeekClient()



class OllamaDeepSeekClientTest(SimpleTestCase):
    def test_chat_returns_response_from_ollama(self):
        ollama = Mock()
        ollama.chat.return_value = {
            "message": {
                "content": "The return policy is 30 days."
            }
        }

        client = OllamaDeepSeekClient(ollama=ollama)

        result = client.chat("What is your return policy?")

        self.assertEqual(result, "The return policy is 30 days.")
        ollama.chat.assert_called_once_with(
            "What is your return policy?"
        )



    def test_stream_yields_message_content(self):
        ollama = Mock()
        ollama.stream.return_value = iter(
            [
                {"message": {"content": "The "}},
                {"message": {"content": "return "}},
                {"message": {"content": "policy "}},
                {"message": {"content": "is 30 days."}},
            ]
        )

        client = OllamaDeepSeekClient(ollama=ollama)

        result = list(client.stream("What is your return policy?"))

        self.assertEqual(
            result,
            ["The ", "return ", "policy ", "is 30 days."],
        )


    
    def test_client_can_be_created_from_configuration(self):
        client = OllamaDeepSeekClient.from_config(
            base_url="http://ollama:11434",
            model="deepseek-r1",
        )

        self.assertEqual(client.base_url, "http://ollama:11434")
        self.assertEqual(client.model, "deepseek-r1")


    @patch("apps.ai.providers.llm.clients.ollama.Client")
    def test_from_config_creates_ollama_client(self, client_class):
        client = Mock()
        client_class.return_value = client

        result = OllamaDeepSeekClient.from_config(
            base_url="http://mac-host:11434",
            model="deepseek-r1",
        )

        client_class.assert_called_once_with(
            host="http://mac-host:11434",
        )

        self.assertIs(result.ollama, client)
        self.assertEqual(result.model, "deepseek-r1")