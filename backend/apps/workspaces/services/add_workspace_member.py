from django.core.exceptions import PermissionDenied
from django.db import transaction
from apps.common.exceptions import AlreadyWorkspaceMemberError
from apps.workspaces.models import (
    WorkspaceMembership,
    WorkspaceRole,
)


class AddWorkspaceMemberService:

    @staticmethod
    @transaction.atomic
    def execute(*, actor, workspace, user):
        is_owner = WorkspaceMembership.objects.filter(
            workspace=workspace,
            user=actor,
            role=WorkspaceRole.OWNER,
        ).exists()

        if not is_owner:
            raise PermissionDenied(
                "Only workspace owners can add staff members."
            )

        existing = WorkspaceMembership.objects.filter(
            workspace=workspace,
            user=user,
        ).exists()

        if existing:
            raise AlreadyWorkspaceMemberError(
                "User is already a member of this workspace."
            )

        membership = WorkspaceMembership.objects.create(
            workspace=workspace,
            user=user,
            role=WorkspaceRole.STAFF,
        )

        return membership