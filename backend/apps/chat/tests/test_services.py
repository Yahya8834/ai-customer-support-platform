from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.chat.services.check_workspace_access import check_workspace_access
from apps.chat.services.check_conversation_access import check_conversation_access
from apps.workspaces.models import Workspace, WorkspaceMembership, WorkspaceRole
from apps.chat.models.conversation import Conversation



User = get_user_model()

class CheckWorkspaceAccessTests(TestCase):

    def setUp(self):
        self.member = User.objects.create_user(
            username="member",
            email="member@example.com",
            password="password123",
        )

        self.outsider = User.objects.create_user(
            username="outsider",
            email="outsider@example.com",
            password="password123",
        )

        self.workspace = Workspace.objects.create(
            name="Workspace A",
            slug="workspace-a",
        )

        WorkspaceMembership.objects.create(
            workspace=self.workspace,
            user=self.member,
            role=WorkspaceRole.OWNER,
        )

    def test_workspace_member_has_access(self):
        result = check_workspace_access(
            actor=self.member,
            workspace=self.workspace,
        )

        self.assertTrue(result)

    def test_non_member_is_denied_access(self):
        with self.assertRaises(PermissionDenied):
            check_workspace_access(
                actor=self.outsider,
                workspace=self.workspace,
            )


class CheckConversationAccessTests(TestCase):
    def test_conversation_belonging_to_workspace_is_allowed(self):
        workspace = Workspace.objects.create(
            name="Workspace A",
            slug="workspace-a",
        )

        conversation = Conversation.objects.create(
            workspace=workspace,
        )

        result = check_conversation_access(
            conversation_uuid=conversation.uuid,
            workspace_uuid=workspace.uuid,
        )

        self.assertTrue(result)

    def test_conversation_from_another_workspace_is_rejected(self):
        workspace_a = Workspace.objects.create(
            name="Workspace A",
            slug="workspace-a",
        )

        workspace_b = Workspace.objects.create(
            name="Workspace B",
            slug="workspace-b",
        )

        conversation = Conversation.objects.create(
            workspace=workspace_b,
        )

        with self.assertRaises(PermissionDenied):
            check_conversation_access(
                conversation_uuid=conversation.uuid,
                workspace_uuid=workspace_a.uuid,
            )