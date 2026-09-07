from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase
from config.asgi import application
from channels.db import database_sync_to_async
from apps.chat.models.conversation import Conversation
from apps.chat.models.message import Message
from apps.workspaces.models import Workspace, WorkspaceMembership
from apps.accounts.models import User



@database_sync_to_async
def message_exists(conversation_uuid, content):
    return Message.objects.filter(
        conversation_id=conversation_uuid,
        role="user",
        content=content,
    ).exists()

class ChatConsumerTests(TransactionTestCase):

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
        
    async def test_received_message_is_persisted_to_conversation(self):
        workspace = await database_sync_to_async(Workspace.objects.create)(
            name="Test Workspace",
            slug="test-workspace",
        )

        workspace_uuid = str(workspace.uuid)
        conversation_uuid = "6ba7b810-9dad-11d1-80b4-00c04fd430c8"

        await database_sync_to_async(Conversation.objects.create)(
            uuid=conversation_uuid,
            workspace=workspace,
        )

        communicator = WebsocketCommunicator(
            application,
            f"/ws/v1/chat/{workspace_uuid}/",
        )

        connected, _ = await communicator.connect()

        self.assertTrue(connected)

        await communicator.receive_from()

        await communicator.send_json_to({
            "conversation_uuid": conversation_uuid,
            "provider": "openrouter",
            "model": "qwen",
            "prompt": "Hello, support!",
        })

        await communicator.disconnect()

        messages = await database_sync_to_async(list)(
            Message.objects.all()
        )

        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0].conversation_id),
            conversation_uuid,
        )
        self.assertEqual(messages[0].role, "user")
        self.assertEqual(messages[0].content, "Hello, support!")

    async def test_message_cannot_be_sent_to_conversation_from_another_workspace(self):
        workspace_a = await database_sync_to_async(Workspace.objects.create)(
            name="Workspace A",
            slug="workspace-a",
        )

        workspace_b = await database_sync_to_async(Workspace.objects.create)(
            name="Workspace B",
            slug="workspace-b",
        )

        conversation = await database_sync_to_async(Conversation.objects.create)(
            workspace=workspace_b,
        )

        communicator = WebsocketCommunicator(
            application,
            f"/ws/v1/chat/{workspace_a.uuid}/",
        )

        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        await communicator.receive_from()

        await communicator.send_json_to({
            "conversation_uuid": str(conversation.uuid),
            "provider": "openrouter",
            "model": "qwen",
            "prompt": "This should not be accepted.",
        })

        response = await communicator.receive_json_from()

        self.assertEqual(
            response,
            {
                "error": "Conversation does not belong to this workspace.",
            },
        )

        await communicator.disconnect()

        messages = await database_sync_to_async(list)(
            Message.objects.all()
        )

        self.assertEqual(messages, [])