from django.core.exceptions import PermissionDenied, ValidationError
from apps.documents.models import Document
from apps.workspaces.models import Workspace, WorkspaceMembership
from apps.common.exceptions import WorkspaceNotFoundError
from apps.documents.events import publishers
from apps.documents.events.contracts import DocumentUploadedEvent


class UploadDocumentService:

    @staticmethod
    def execute(*, user, workspace_uuid, file):
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

        if file.content_type != "application/pdf":
            raise ValidationError(
                "Only PDF documents are supported."
            )
        
        if file.size == 0:
            raise ValidationError(
                "The uploaded file cannot be empty."
            )
        

        document = Document.objects.create(
            workspace=workspace,
            uploaded_by=user,
            file=file,
            original_filename=file.name,
            content_type=file.content_type,
            file_size=file.size,
        )

        event = DocumentUploadedEvent(
            document_uuid=document.uuid,
            workspace_uuid=document.workspace.uuid,
            uploaded_by_uuid=document.uploaded_by.uuid
        )

        publishers.publish_document_uploaded(event=event)

        return document
    

