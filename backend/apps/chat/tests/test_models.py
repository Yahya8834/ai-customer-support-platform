import uuid
from django.test import TestCase
from apps.chat.models.conversation import Conversation
from apps.workspaces.models import Workspace
from apps.chat.models.message import Message



class ConversationModelTests(TestCase):

    def setUp(self):
        self.workspace = Workspace.objects.create(
            name="Test Workspace",
            slug="test-workspace",
        )

    def test_conversation_has_uuid_primary_key(self):
        conversation = Conversation.objects.create(
            workspace=self.workspace,
        )

        self.assertIsInstance(conversation.uuid, uuid.UUID)
        self.assertIsNotNone(conversation.uuid)

    def test_conversation_belongs_to_workspace(self):
        conversation = Conversation.objects.create(
            workspace=self.workspace,
        )

        self.assertEqual(conversation.workspace, self.workspace)

    def test_conversation_has_timestamps(self):
        conversation = Conversation.objects.create(
            workspace=self.workspace,
        )

        self.assertIsNotNone(conversation.created_at)
        self.assertIsNotNone(conversation.updated_at)

    def test_conversation_is_deleted_when_workspace_is_deleted(self):
        conversation = Conversation.objects.create(
            workspace=self.workspace,
        )

        conversation_uuid = conversation.uuid

        self.workspace.delete()

        self.assertFalse(
            Conversation.objects.filter(
                uuid=conversation_uuid,
            ).exists()
        )


class MessageModelTests(TestCase):

    def setUp(self):
        self.workspace = Workspace.objects.create(
            name="Test Workspace",
            slug="test-workspace",
        )
        self.conversation = Conversation.objects.create(
            workspace=self.workspace,
        )

    def test_message_has_uuid_primary_key(self):
        message = Message.objects.create(
            conversation=self.conversation,
            role="user",
            content="Hello",
        )

        self.assertIsInstance(message.uuid, uuid.UUID)
        self.assertIsNotNone(message.uuid)

    def test_message_belongs_to_conversation(self):
        message = Message.objects.create(
            conversation=self.conversation,
            role="user",
            content="Hello",
        )

        self.assertEqual(message.conversation, self.conversation)

    def test_message_stores_role_and_content(self):
        message = Message.objects.create(
            conversation=self.conversation,
            role="user",
            content="Hello",
        )

        self.assertEqual(message.role, "user")
        self.assertEqual(message.content, "Hello")

    def test_message_has_created_at_timestamp(self):
        message = Message.objects.create(
            conversation=self.conversation,
            role="user",
            content="Hello",
        )

        self.assertIsNotNone(message.created_at)

    def test_message_is_deleted_when_conversation_is_deleted(self):
        message = Message.objects.create(
            conversation=self.conversation,
            role="user",
            content="Hello",
        )

        message_uuid = message.uuid

        self.conversation.delete()

        self.assertFalse(
            Message.objects.filter(
                uuid=message_uuid,
            ).exists()
        )

    def test_conversation_has_related_messages(self):
        message = Message.objects.create(
            conversation=self.conversation,
            role="user",
            content="Hello",
        )

        self.assertIn(
            message,
            self.conversation.messages.all(),
        )