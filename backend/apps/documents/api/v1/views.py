from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework import status
from apps.documents.api.common.serializers import DocumentSerializer
from apps.documents.selectors.list_workspace_documents import (
    list_workspace_documents,
)
from apps.documents.services.upload_document import UploadDocumentService
from apps.documents.selectors.get_document import get_document
from apps.common.exceptions import DocumentNotFoundError, WorkspaceNotFoundError
from apps.documents.services.delete_document import DeleteDocumentService
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError


class DocumentsView(APIView):
    def get(self, request, workspace_uuid):
        documents = list_workspace_documents(
            user=request.user,
            workspace_uuid=workspace_uuid,
        )

        serializer = DocumentSerializer(
            documents,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request, workspace_uuid):
        try:
            document = UploadDocumentService.execute(
                user=request.user,
                workspace_uuid=workspace_uuid,
                file=request.FILES["file"],
            )

        except ValidationError as exc:
            raise DRFValidationError(exc.messages)


        serializer = DocumentSerializer(document)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )
    


class RetrieveDocumentView(APIView):

    def get(self, request, workspace_uuid, document_uuid):
        try:
            document = get_document(
                user=request.user,
                workspace_uuid=workspace_uuid,
                document_uuid=document_uuid,
            )

        except DocumentNotFoundError:
            raise NotFound(
                "Document not found."
            )

        serializer = DocumentSerializer(document)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    

    def delete(self, request, workspace_uuid, document_uuid):
        try:
            DeleteDocumentService.execute(
                user=request.user,
                workspace_uuid=workspace_uuid,
                document_uuid=document_uuid,
            )

        except WorkspaceNotFoundError:
            raise NotFound(
                "Workspace not found."
            )

        except DocumentNotFoundError:
            raise NotFound(
                "Document not found."
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )