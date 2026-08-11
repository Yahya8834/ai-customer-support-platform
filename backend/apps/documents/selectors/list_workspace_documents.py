from django.core.exceptions import PermissionDenied

from apps.documents.models import Document
from apps.common.exceptions import WorkspaceNotFoundError
from apps.workspaces.models import Workspace, WorkspaceMembership


def list_workspace_documents(*, user, workspace_uuid):
    try:
        workspace = Workspace.objects.get(uuid=workspace_uuid)
    except Workspace.DoesNotExist:
        raise WorkspaceNotFoundError(
            "Workspace does not exist."
        )

    is_member = WorkspaceMembership.objects.filter(
        workspace=workspace,
        user=user,
    ).exists()

    if not is_member:
        raise PermissionDenied(
            "You are not a member of this workspace."
        )

    return Document.objects.filter(
        workspace=workspace,
    )