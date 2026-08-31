from django.test import TestCase
from apps.chat.models.conversation import Conversation
from apps.chat.selectors.list_workspace_conversations import (
    list_workspace_conversations,
)
from apps.workspaces.models import Workspace



class ListWorkspaceConversationsTests(TestCase):

    def setUp(self):
        self.workspace = Workspace.objects.create(
            name="Workspace A",
            slug="workspace-a",
        )
        self.other_workspace = Workspace.objects.create(
            name="Workspace B",
            slug="workspace-b",
        )

        self.conversation = Conversation.objects.create(
            workspace=self.workspace,
        )
        self.other_conversation = Conversation.objects.create(
            workspace=self.other_workspace,
        )

    def test_returns_only_workspace_conversations(self):
        conversations = list_workspace_conversations(
            workspace_uuid=self.workspace.uuid,
        )

        self.assertEqual(
            list(conversations),
            [self.conversation],
        )

    def test_does_not_return_other_workspace_conversations(self):
        conversations = list_workspace_conversations(
            workspace_uuid=self.workspace.uuid,
        )

        self.assertNotIn(
            self.other_conversation,
            conversations,
        )