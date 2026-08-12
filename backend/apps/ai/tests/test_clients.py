from django.test import SimpleTestCase
from backend.apps.ai.providers.llm.clients.deepseek import DeepSeekClient

class DeepSeekClientTest(SimpleTestCase):
    def test_client_requires_chat_and_stream(self):
        with self.assertRaises(TypeError):
            DeepSeekClient()