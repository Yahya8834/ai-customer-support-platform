from rest_framework import serializers
from apps.workspaces.models import Workspace, WorkspaceMembership

class CreateWorkspaceSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=255,
        trim_whitespace=True,
    )


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = (
            "uuid",
            "name",
            "slug",
            "created_at",
            "updated_at",
        )


class AddWorkspaceMemberSerializer(serializers.Serializer):
    user_uuid = serializers.UUIDField()


class WorkspaceMembershipSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )

    class Meta:
        model = WorkspaceMembership
        fields = (
            "uuid",
            "username",
            "email",
            "role",
            "created_at",
        )