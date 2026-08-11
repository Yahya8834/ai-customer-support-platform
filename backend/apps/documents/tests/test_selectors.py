import uuid
from django.core.exceptions import PermissionDenied
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from apps.accounts.models import User
from apps.documents.selectors.list_workspace_documents import list_workspace_documents
from apps.documents.selectors.get_document import get_document
from apps.common.exceptions import DocumentNotFoundError, WorkspaceNotFoundError
from apps.documents.services.upload_document import UploadDocumentService
from apps.workspaces.services.add_workspace_member import AddWorkspaceMemberService
from apps.workspaces.services.create_workspace import CreateWorkspaceService




class ListWorkspaceDocumentsSelectorTests(TestCase):
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

        self.document = UploadDocumentService.execute(
            user=self.owner,
            workspace_uuid=self.workspace.uuid,
            file=self.pdf,
        )

    def test_owner_can_list_workspace_documents(self):
        documents = list_workspace_documents(
            user=self.owner,
            workspace_uuid=self.workspace.uuid,
        )

        self.assertEqual(documents.count(), 1)
        self.assertEqual(documents.first(), self.document)

    def test_staff_can_list_workspace_documents(self):
        documents = list_workspace_documents(
            user=self.staff,
            workspace_uuid=self.workspace.uuid,
        )

        self.assertEqual(documents.count(), 1)
        self.assertEqual(documents.first(), self.document)

    def test_non_member_cannot_list_workspace_documents(self):
        with self.assertRaises(PermissionDenied):
            list_workspace_documents(
                user=self.outsider,
                workspace_uuid=self.workspace.uuid,
            )




class GetDocumentSelectorTests(TestCase):
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

    def test_owner_can_retrieve_document(self):
        document = get_document(
            user=self.owner,
            workspace_uuid=self.workspace.uuid,
            document_uuid=self.document.uuid,
        )

        self.assertEqual(
            document,
            self.document,
        )


    def test_staff_can_retrieve_document(self):
        document = get_document(
            user=self.staff,
            workspace_uuid=self.workspace.uuid,
            document_uuid=self.document.uuid,
        )

        self.assertEqual(
            document,
            self.document,
        )
    def test_non_member_cannot_retrieve_document(self):
        with self.assertRaises(PermissionDenied):
            get_document(
                user=self.outsider,
                workspace_uuid=self.workspace.uuid,
                document_uuid=self.document.uuid,
            )

    def test_workspace_must_exist(self):
        with self.assertRaises(WorkspaceNotFoundError):
            get_document(
                user=self.owner,
                workspace_uuid=uuid.uuid4(),
                document_uuid=self.document.uuid,
            )

    def test_document_must_exist_in_workspace(self):
        with self.assertRaises(DocumentNotFoundError):
            get_document(
                user=self.owner,
                workspace_uuid=self.workspace.uuid,
                document_uuid=uuid.uuid4(),
            )