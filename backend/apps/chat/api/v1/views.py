from rest_framework.response import Response
from rest_framework.views import APIView
from apps.chat.api.common.serializers import ConversationSerializer, MessageSerializer
from apps.chat.selectors.list_workspace_conversations import list_workspace_conversations
from apps.chat.selectors.list_conversation_messages import list_conversation_messages
from apps.chat.services.check_workspace_access import check_workspace_access
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from apps.workspaces.models import Workspace
from apps.chat.models.conversation import Conversation




class ConversationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, workspace_uuid):
        workspace = get_object_or_404(
            Workspace,
            uuid=workspace_uuid,
        )

        check_workspace_access(
            actor=request.user,
            workspace=workspace,
        )

        conversations = list_workspace_conversations(
            workspace_uuid=workspace.uuid,
        )

        serializer = ConversationSerializer(
            conversations,
            many=True,
        )

        return Response(serializer.data)
    

class ConversationMessageListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, workspace_uuid, conversation_uuid):
        workspace = get_object_or_404(
            Workspace,
            uuid=workspace_uuid,
        )

        check_workspace_access(
            actor=request.user,
            workspace=workspace,
        )

        conversation = get_object_or_404(
            Conversation,
            uuid=conversation_uuid,
            workspace=workspace,
        )

        messages = list_conversation_messages(
            conversation_uuid=conversation.uuid,
        )

        serializer = MessageSerializer(
            messages,
            many=True,
        )

        return Response(serializer.data)