from django.test import SimpleTestCase

from apps.ai.providers.llm.clients.base import DeepSeekClient


class DeepSeekClientTest(SimpleTestCase):
    def test_client_requires_chat_and_stream(self):
        with self.assertRaises(TypeError):
            DeepSeekClient()