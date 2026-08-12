from django.test import SimpleTestCase
from apps.ai.providers.llm.clients.deepseek import DeepSeekClient
from unittest.mock import Mock
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