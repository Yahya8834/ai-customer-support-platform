from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.workspaces.services.list_workspace_members import ListWorkspaceMembersService
from apps.workspaces.api.common.serializers import (
    CreateWorkspaceSerializer,
    WorkspaceSerializer,
    AddWorkspaceMemberSerializer,
    WorkspaceMembershipSerializer,
)
from apps.workspaces.selectors.get_user_workspaces import get_user_workspaces
from apps.workspaces.services.create_workspace import CreateWorkspaceService
from apps.workspaces.services.add_workspace_member import AddWorkspaceMemberService
from apps.workspaces.models import Workspace
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404




User = get_user_model()


class WorkspaceListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        workspaces = get_user_workspaces(request.user)

        serializer = WorkspaceSerializer(
            workspaces,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = CreateWorkspaceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        workspace = CreateWorkspaceService.execute(
            user=request.user,
            name=serializer.validated_data["name"],
        )

        return Response(
            WorkspaceSerializer(workspace).data,
            status=status.HTTP_201_CREATED,
        )
    


class AddWorkspaceMemberView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, workspace_uuid):
        serializer = AddWorkspaceMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        workspace = get_object_or_404(
            Workspace,
            uuid=workspace_uuid,
        )

        user = get_object_or_404(
            User,
            uuid=serializer.validated_data["user_uuid"],
        )

        membership = AddWorkspaceMemberService.execute(
            actor=request.user,
            workspace=workspace,
            user=user,
        )

        return Response(
            {
                "uuid": membership.uuid,
                "user_uuid": str(membership.user.pk),
                "workspace_uuid": str(membership.workspace.pk),
                "role": membership.role,
            },
            status=status.HTTP_201_CREATED,
        )
    

    def get(self, request, workspace_uuid):
        workspace = get_object_or_404(
            Workspace,
            uuid=workspace_uuid,
        )

        memberships = ListWorkspaceMembersService.execute(
            actor=request.user,
            workspace=workspace,
        )

        serializer = WorkspaceMembershipSerializer(
            memberships,
            many=True,
        )

        return Response(serializer.data)