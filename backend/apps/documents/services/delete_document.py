from django.core.exceptions import PermissionDenied
from apps.common.exceptions import (
    DocumentNotFoundError,
    WorkspaceNotFoundError,
)
from apps.documents.models import Document
from apps.workspaces.models import (
    Workspace,
    WorkspaceMembership,
)



class DeleteDocumentService:

    @staticmethod
    def execute(*, user, workspace_uuid, document_uuid):
        try:
            workspace = Workspace.objects.get(
                uuid=workspace_uuid,
            )
        except Workspace.DoesNotExist:
            raise WorkspaceNotFoundError(
                "Workspace not found."
            )

        is_member = WorkspaceMembership.objects.filter(
            workspace=workspace,
            user=user,
        ).exists()

        if not is_member:
            raise PermissionDenied(
                "You are not a member of this workspace."
            )

        try:
            document = Document.objects.get(
                uuid=document_uuid,
                workspace=workspace,
            )
        except Document.DoesNotExist:
            raise DocumentNotFoundError(
                "Document not found."
            )

        document.delete()