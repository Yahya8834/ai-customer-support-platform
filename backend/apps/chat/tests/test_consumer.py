from channels.testing import WebsocketCommunicator
from django.test import SimpleTestCase
from config.asgi import application



class ChatConsumerTests(SimpleTestCase):

    async def test_websocket_connection(self):
        communicator = WebsocketCommunicator(
            application,
            "/ws/v1/chat/",
        )

        connected, _ = await communicator.connect()

        self.assertTrue(connected)

        response = await communicator.receive_from()

        self.assertEqual(
            response,
            "connected",
        )

        await communicator.disconnect()