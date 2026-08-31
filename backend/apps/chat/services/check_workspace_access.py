from django.core.exceptions import PermissionDenied
from apps.workspaces.models import WorkspaceMembership



def check_workspace_access(*, actor, workspace):
    is_member = WorkspaceMembership.objects.filter(
        workspace=workspace,
        user=actor,
    ).exists()

    if not is_member:
        raise PermissionDenied(
            "You are not a member of this workspace."
        )

    return True