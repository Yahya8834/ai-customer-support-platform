from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from django.test import SimpleTestCase
from config.asgi import application



class ChatConsumerTests(SimpleTestCase):

    async def test_websocket_connection_joins_workspace_group(self):
        workspace_uuid = "550e8400-e29b-41d4-a716-446655440000"

        communicator = WebsocketCommunicator(
            application,
            f"/ws/v1/chat/{workspace_uuid}/",
        )

        connected, _ = await communicator.connect()

        self.assertTrue(connected)

        response = await communicator.receive_from()

        self.assertEqual(
            response,
            "connected",
        )

        await communicator.disconnect()

    async def test_workspace_group_message_is_sent_to_websocket(self):
        workspace_uuid = "550e8400-e29b-41d4-a716-446655440000"

        communicator = WebsocketCommunicator(
            application,
            f"/ws/v1/chat/{workspace_uuid}/",
        )

        connected, _ = await communicator.connect()

        self.assertTrue(connected)

        await communicator.receive_from()

        channel_layer = get_channel_layer()

        await channel_layer.group_send(
            f"workspace_{workspace_uuid}",
            {
                "type": "chat.message",
                "token": "return",
            },
        )

        response = await communicator.receive_from()

        self.assertEqual(
            response,
            '{"token": "return"}',
        )

        await communicator.disconnect()