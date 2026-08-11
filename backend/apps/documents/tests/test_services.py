import uuid
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.accounts.models import User
from apps.documents.models import Document
from apps.workspaces.models import Workspace
from apps.documents.services.upload_document import UploadDocumentService
from apps.workspaces.services.create_workspace import CreateWorkspaceService
from apps.workspaces.services.add_workspace_member import AddWorkspaceMemberService
from apps.common.exceptions import WorkspaceNotFoundError, DocumentNotFoundError
from apps.documents.services.delete_document import DeleteDocumentService
from apps.documents.events import publishers
from apps.documents.events.contracts import DocumentUploadedEvent
from unittest.mock import patch



class UploadDocumentServiceTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="password123",
        )

        self.staff = User.objects.create_user(
            username="staff",
            email="staff@example.com",
            password="password123",
        )

        self.outsider = User.objects.create_user(
            username="outsider",
            email="outsider@example.com",
            password="password123",
        )

        self.workspace = CreateWorkspaceService.execute(
            user=self.owner,
            name="Acme Support",
        )

        AddWorkspaceMemberService.execute(
            actor=self.owner,
            workspace=self.workspace,
            user=self.staff,
        )

        self.pdf = SimpleUploadedFile(
            name="support-guide.pdf",
            content=b"%PDF-1.4 fake pdf content",
            content_type="application/pdf",
        )

    def test_owner_can_upload_pdf(self):
        document = UploadDocumentService.execute(
            user=self.owner,
            workspace_uuid=self.workspace.uuid,
            file=self.pdf,
        )

        self.assertIsInstance(document, Document)
        self.assertEqual(document.workspace, self.workspace)
        self.assertEqual(document.uploaded_by, self.owner)
        self.assertEqual(document.original_filename, self.pdf.name)
        self.assertEqual(document.content_type, self.pdf.content_type)
        self.assertEqual(document.file_size, self.pdf.size)
        self.assertEqual(
            document.processing_status,
            Document.ProcessingStatus.UPLOADED,
        )

    def test_staff_can_upload_pdf(self):
        document = UploadDocumentService.execute(
            user=self.staff,
            workspace_uuid=self.workspace.uuid,
            file=self.pdf,
        )

        self.assertEqual(document.workspace, self.workspace)
        self.assertEqual(document.uploaded_by, self.staff)

    def test_non_member_cannot_upload_pdf(self):
        with self.assertRaises(PermissionDenied):
            UploadDocumentService.execute(
                user=self.outsider,
                workspace_uuid=self.workspace.uuid,
                file=self.pdf,
            )

    def test_cannot_upload_non_pdf_file(self):
        text_file = SimpleUploadedFile(
            name="notes.txt",
            content=b"Hello, world!",
            content_type="text/plain",
        )

        with self.assertRaises(ValidationError):
            UploadDocumentService.execute(
                user=self.owner,
                workspace_uuid=self.workspace.uuid,
                file=text_file,
            )

    def test_cannot_upload_empty_pdf(self):
        empty_pdf = SimpleUploadedFile(
            name="empty.pdf",
            content=b"",
            content_type="application/pdf",
        )

        with self.assertRaises(ValidationError):
            UploadDocumentService.execute(
                user=self.owner,
                workspace_uuid=self.workspace.uuid,
                file=empty_pdf,
            )

    
    def test_workspace_must_exist(self):
        with self.assertRaises(WorkspaceNotFoundError):
            UploadDocumentService.execute(
                user=self.owner,
                workspace_uuid=uuid.uuid4(),
                file=self.pdf,
            )




    @patch("apps.documents.services.upload_document.publishers.publish_document_uploaded")
    def test_upload_document_publishes_document_uploaded_event(
        self,
        mock_publish_document_uploaded,
    ):
        document = UploadDocumentService.execute(
            user=self.owner,
            workspace_uuid=self.workspace.uuid,
            file=self.pdf,
        )

        mock_publish_document_uploaded.assert_called_once_with(
            event=DocumentUploadedEvent(
                document_uuid=document.uuid,
                workspace_uuid=document.workspace.uuid,
                uploaded_by_uuid=document.uploaded_by.uuid,
            ),
        )



class DeleteDocumentServiceTests(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="password123",
        )

        self.staff = User.objects.create_user(
            username="staff",
            email="staff@example.com",
            password="password123",
        )

        self.outsider = User.objects.create_user(
            username="outsider",
            email="outsider@example.com",
            password="password123",
        )

        self.workspace = CreateWorkspaceService.execute(
            user=self.owner,
            name="Acme Support",
        )

        AddWorkspaceMemberService.execute(
            actor=self.owner,
            workspace=self.workspace,
            user=self.staff,
        )

        pdf = SimpleUploadedFile(
            name="support-guide.pdf",
            content=b"%PDF-1.4 fake pdf content",
            content_type="application/pdf",
        )

        self.document = UploadDocumentService.execute(
            user=self.owner,
            workspace_uuid=self.workspace.uuid,
            file=pdf,
        )

    def test_owner_can_delete_document(self):
        DeleteDocumentService.execute(
            user=self.owner,
            workspace_uuid=self.workspace.uuid,
            document_uuid=self.document.uuid,
        )

        self.assertFalse(
            Document.objects.filter(
                uuid=self.document.uuid,
            ).exists()
        )

    def test_staff_can_delete_document(self):
        DeleteDocumentService.execute(
            user=self.staff,
            workspace_uuid=self.workspace.uuid,
            document_uuid=self.document.uuid,
        )

        self.assertFalse(
            Document.objects.filter(
                uuid=self.document.uuid,
            ).exists()
        )

    def test_non_member_cannot_delete_document(self):
        with self.assertRaises(PermissionDenied):
            DeleteDocumentService.execute(
                user=self.outsider,
                workspace_uuid=self.workspace.uuid,
                document_uuid=self.document.uuid,
            )

    def test_document_not_found_in_workspace(self):
        with self.assertRaises(DocumentNotFoundError):
            DeleteDocumentService.execute(
                user=self.owner,
                workspace_uuid=self.workspace.uuid,
                document_uuid=uuid.uuid4(),
            )