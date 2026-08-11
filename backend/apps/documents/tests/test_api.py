import uuid
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.accounts.models import User
from apps.documents.models import Document
from apps.documents.services.upload_document import UploadDocumentService
from apps.workspaces.services.create_workspace import (
    CreateWorkspaceService,
)
from apps.workspaces.services.add_workspace_member import AddWorkspaceMemberService


class ListWorkspaceDocumentsAPITests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="password123",
        )

        self.workspace = CreateWorkspaceService.execute(
            user=self.owner,
            name="Acme Support",
        )

        pdf = SimpleUploadedFile(
            name="support-guide.pdf",
            content=b"%PDF-1.4 fake pdf content",
            content_type="application/pdf",
        )

        UploadDocumentService.execute(
            user=self.owner,
            workspace_uuid=self.workspace.uuid,
            file=pdf,
        )

        self.staff = User.objects.create_user(
            username="staff",
            email="staff@example.com",
            password="password123",
        )

        AddWorkspaceMemberService.execute(
            actor=self.owner,
            workspace=self.workspace,
            user=self.staff,
        )

        self.client.force_authenticate(
            user=self.owner,
        )

    def test_owner_can_list_workspace_documents(self):
        url = reverse(
            "documents:workspace-documents",
            kwargs={
                "workspace_uuid": self.workspace.uuid,
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["original_filename"],
            "support-guide.pdf",
        )

    def test_staff_can_list_workspace_documents(self):
        self.client.force_authenticate(
            user=self.staff,
        )

        url = reverse(
            "documents:workspace-documents",
            kwargs={
                "workspace_uuid": self.workspace.uuid,
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["original_filename"],
            "support-guide.pdf",
        )

    def test_non_member_cannot_list_workspace_documents(self):
        outsider = User.objects.create_user(
            username="outsider",
            email="outsider@example.com",
            password="password123",
        )

        self.client.force_authenticate(
            user=outsider,
        )

        url = reverse(
            "documents:workspace-documents",
            kwargs={
                "workspace_uuid": self.workspace.uuid,
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )



class UploadDocumentAPITests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="password123",
        )

        self.workspace = CreateWorkspaceService.execute(
            user=self.owner,
            name="Acme Support",
        )

        self.staff = User.objects.create_user(
            username="staff",
            email="staff@example.com",
            password="password123",
        )

        AddWorkspaceMemberService.execute(
            actor=self.owner,
            workspace=self.workspace,
            user=self.staff,
        )

        self.client.force_authenticate(
            user=self.owner,
        )


    def test_owner_can_upload_pdf(self):
        pdf = SimpleUploadedFile(
            name="support-guide.pdf",
            content=b"%PDF-1.4 fake pdf content",
            content_type="application/pdf",
        )

        url = reverse(
            "documents:workspace-documents",
            kwargs={
                "workspace_uuid": self.workspace.uuid,
            },
        )

        response = self.client.post(
            url,
            data={
                "file": pdf,
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Document.objects.count(),
            1,
        )

        document = Document.objects.first()

        self.assertEqual(
            document.uploaded_by,
            self.owner,
        )

        self.assertEqual(
            document.workspace,
            self.workspace,
        )

    def test_staff_can_upload_pdf(self):
        self.client.force_authenticate(
            user=self.staff,
        )

        pdf = SimpleUploadedFile(
            name="staff-guide.pdf",
            content=b"%PDF-1.4 fake pdf content",
            content_type="application/pdf",
        )

        url = reverse(
            "documents:workspace-documents",
            kwargs={
                "workspace_uuid": self.workspace.uuid,
            },
        )

        response = self.client.post(
            url,
            data={
                "file": pdf,
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Document.objects.count(),
            1,
        )

        document = Document.objects.first()

        self.assertEqual(
            document.uploaded_by,
            self.staff,
        )

        self.assertEqual(
            document.workspace,
            self.workspace,
        )

        self.assertEqual(
            document.original_filename,
            "staff-guide.pdf",
        )


    def test_cannot_upload_non_pdf_file(self):
        self.client.force_authenticate(
            user=self.owner,
        )

        png = SimpleUploadedFile(
            name="logo.png",
            content=b"fake png content",
            content_type="image/png",
        )

        url = reverse(
            "documents:workspace-documents",
            kwargs={
                "workspace_uuid": self.workspace.uuid,
            },
        )

        response = self.client.post(
            url,
            data={
                "file": png,
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn(
            "Only PDF documents are supported.",
            str(response.data),
        )

        self.assertEqual(
            Document.objects.count(),
            0,
        )


class RetrieveDocumentAPITests(APITestCase):
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
        self.client.force_authenticate(
            user=self.owner,
        )

        url = reverse(
            "documents:workspace-document-detail",
            kwargs={
                "workspace_uuid": self.workspace.uuid,
                "document_uuid": self.document.uuid,
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["original_filename"],
            "support-guide.pdf",
        )

        self.assertEqual(
            self.document.workspace,
            self.workspace,
        )

        self.assertIsNotNone(
            self.document.uuid,
        )


    def test_staff_can_retrieve_document(self):
        self.client.force_authenticate(
            user=self.staff,
        )

        url = reverse(
            "documents:workspace-document-detail",
            kwargs={
                "workspace_uuid": self.workspace.uuid,
                "document_uuid": self.document.uuid,
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["original_filename"],
            "support-guide.pdf",
        )


    def test_non_member_cannot_retrieve_document(self):
        self.client.force_authenticate(
            user=self.outsider,
        )

        url = reverse(
            "documents:workspace-document-detail",
            kwargs={
                "workspace_uuid": self.workspace.uuid,
                "document_uuid": self.document.uuid,
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )


    def test_document_not_found_in_workspace(self):
        self.client.force_authenticate(
            user=self.owner,
        )

        url = reverse(
            "documents:workspace-document-detail",
            kwargs={
                "workspace_uuid": self.workspace.uuid,
                "document_uuid": uuid.uuid4(),
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )



class DeleteDocumentAPITests(APITestCase):

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
        self.client.force_authenticate(
            user=self.owner,
        )

        url = reverse(
            "documents:workspace-document-detail",
            kwargs={
                "workspace_uuid": self.workspace.uuid,
                "document_uuid": self.document.uuid,
            },
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Document.objects.filter(
                uuid=self.document.uuid,
            ).exists()
        )

    def test_staff_can_delete_document(self):
        self.client.force_authenticate(
            user=self.staff,
        )

        url = reverse(
            "documents:workspace-document-detail",
            kwargs={
                "workspace_uuid": self.workspace.uuid,
                "document_uuid": self.document.uuid,
            },
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Document.objects.filter(
                uuid=self.document.uuid,
            ).exists()
        )

    def test_non_member_cannot_delete_document(self):
        self.client.force_authenticate(
            user=self.outsider,
        )

        url = reverse(
            "documents:workspace-document-detail",
            kwargs={
                "workspace_uuid": self.workspace.uuid,
                "document_uuid": self.document.uuid,
            },
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_document_not_found_in_workspace(self):
        self.client.force_authenticate(
            user=self.owner,
        )

        url = reverse(
            "documents:workspace-document-detail",
            kwargs={
                "workspace_uuid": self.workspace.uuid,
                "document_uuid": uuid.uuid4(),
            },
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )