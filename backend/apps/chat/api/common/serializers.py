from rest_framework import serializers
from apps.chat.models.conversation import Conversation
from apps.chat.models.message import Message



class ConversationSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format="hex_verbose")
    workspace = serializers.UUIDField(
        source="workspace.uuid",
        read_only=True,
        format="hex_verbose",
    )

    class Meta:
        model = Conversation
        fields = [
            "uuid",
            "workspace",
            "created_at",
            "updated_at",
        ]


class MessageSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format="hex_verbose")
    conversation = serializers.UUIDField(source="conversation.uuid")

    class Meta:
        model = Message
        fields = [
            "uuid",
            "conversation",
            "role",
            "content",
            "created_at",
        ]