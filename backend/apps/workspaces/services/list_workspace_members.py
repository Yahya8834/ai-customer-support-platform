from django.core.exceptions import PermissionDenied
from apps.workspaces.models import WorkspaceMembership


class ListWorkspaceMembersService:

    @staticmethod
    def execute(*, actor, workspace):
        is_member = WorkspaceMembership.objects.filter(
            workspace=workspace,
            user=actor,
        ).exists()

        if not is_member:
            raise PermissionDenied(
                "You are not a member of this workspace."
            )

        return WorkspaceMembership.objects.filter(
            workspace=workspace,
        )