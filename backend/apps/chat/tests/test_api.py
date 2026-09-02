from django.test import TestCase
from rest_framework.test import APIClient
from apps.chat.models.conversation import Conversation
from apps.chat.models.message import Message
from apps.workspaces.models import Workspace, WorkspaceMembership, WorkspaceRole
from apps.chat.api.common.serializers import ConversationSerializer, MessageSerializer
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken




User = get_user_model()

class ConversationListAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="member",
            email="member@example.com",
            password="password123",
        )

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.workspace = Workspace.objects.create(
            name="Workspace A",
            slug="workspace-a",
        )

        WorkspaceMembership.objects.create(
            workspace=self.workspace,
            user=self.user,
            role=WorkspaceRole.OWNER,
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

        self.url = (
            f"/api/v1/workspaces/"
            f"{self.workspace.uuid}/conversations/"
        )

    def authenticate(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

    def test_workspace_member_can_list_conversations(self):
        self.authenticate()

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(len(response.data), 1)

        self.assertEqual(
            response.data[0]["uuid"],
            str(self.conversation.uuid),
        )

    def test_workspace_member_cannot_see_other_workspace_conversations(self):
        self.authenticate()

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        returned_uuids = {
            item["uuid"]
            for item in response.data
        }

        self.assertNotIn(
            str(self.other_conversation.uuid),
            returned_uuids,
        )

    def test_unauthenticated_user_cannot_list_conversations(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
    
    def test_non_member_cannot_list_workspace_conversations(self):
        outsider = User.objects.create_user(
            username="outsider",
            email="outsider@example.com",
            password="password123",
        )

        outsider_token = str(
            RefreshToken.for_user(outsider).access_token
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {outsider_token}"
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_nonexistent_workspace_returns_404(self):
        self.authenticate()

        nonexistent_workspace_uuid = (
            "550e8400-e29b-41d4-a716-446655440000"
        )

        response = self.client.get(
            f"/api/v1/workspaces/"
            f"{nonexistent_workspace_uuid}/conversations/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
        

class ConversationSerializerTests(TestCase):

    def setUp(self):
        self.workspace = Workspace.objects.create(
            name="Workspace A",
            slug="workspace-a",
        )
        self.conversation = Conversation.objects.create(
            workspace=self.workspace,
        )

    def test_serializes_conversation(self):
        serializer = ConversationSerializer(
            self.conversation,
        )

        self.assertEqual(
            serializer.data["uuid"],
            str(self.conversation.uuid),
        )
        self.assertEqual(
            serializer.data["workspace"],
            str(self.workspace.uuid),
        )
        self.assertIn("created_at", serializer.data)
        self.assertIn("updated_at", serializer.data)


class ConversationMessageListAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="member",
            email="member@example.com",
            password="password123",
        )

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.workspace = Workspace.objects.create(
            name="Workspace A",
            slug="workspace-a",
        )

        WorkspaceMembership.objects.create(
            workspace=self.workspace,
            user=self.user,
            role=WorkspaceRole.OWNER,
        )

        self.conversation = Conversation.objects.create(
            workspace=self.workspace,
        )

        self.message = Message.objects.create(
            conversation=self.conversation,
            role="user",
            content="Hello",
        )

        self.url = (
            f"/api/v1/workspaces/{self.workspace.uuid}/"
            f"conversations/{self.conversation.uuid}/messages/"
        )

    def authenticate(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

    def test_workspace_member_can_list_conversation_messages(self):
        self.authenticate()

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(len(response.data), 1)

        self.assertEqual(
            response.data[0]["uuid"],
            str(self.message.uuid),
        )

        self.assertEqual(
            response.data[0]["role"],
            "user",
        )

        self.assertEqual(
            response.data[0]["content"],
            "Hello",
        )

    def test_only_messages_from_requested_conversation_are_returned(self):
        other_conversation = Conversation.objects.create(
            workspace=self.workspace,
        )

        other_message = Message.objects.create(
            conversation=other_conversation,
            role="assistant",
            content="This belongs elsewhere",
        )

        self.authenticate()

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        returned_uuids = {
            message["uuid"]
            for message in response.data
        }

        self.assertIn(
            str(self.message.uuid),
            returned_uuids,
        )

        self.assertNotIn(
            str(other_message.uuid),
            returned_uuids,
        )
    
    def test_cannot_access_conversation_from_another_workspace(self):
        other_workspace = Workspace.objects.create(
            name="Workspace B",
            slug="workspace-b",
        )

        other_conversation = Conversation.objects.create(
            workspace=other_workspace,
        )

        Message.objects.create(
            conversation=other_conversation,
            role="user",
            content="Private message",
        )

        self.authenticate()

        response = self.client.get(
            f"/api/v1/workspaces/{self.workspace.uuid}/"
            f"conversations/{other_conversation.uuid}/messages/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_non_member_cannot_list_conversation_messages(self):
        outsider = User.objects.create_user(
            username="outsider",
            email="outsider@example.com",
            password="password123",
        )

        outsider_token = str(
            RefreshToken.for_user(outsider).access_token
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {outsider_token}"
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )


class MessageSerializerTests(TestCase):

    def setUp(self):
        self.workspace = Workspace.objects.create(
            name="Workspace A",
            slug="workspace-a",
        )

        self.conversation = Conversation.objects.create(
            workspace=self.workspace,
        )

        self.message = Message.objects.create(
            conversation=self.conversation,
            role="user",
            content="Hello",
        )

    def test_serializes_message(self):
        serializer = MessageSerializer(
            self.message,
        )

        self.assertEqual(
            serializer.data["uuid"],
            str(self.message.uuid),
        )

        self.assertEqual(
            serializer.data["conversation"],
            str(self.conversation.uuid),
        )

        self.assertEqual(
            serializer.data["role"],
            "user",
        )

        self.assertEqual(
            serializer.data["content"],
            "Hello",
        )

        self.assertIn("created_at", serializer.data)