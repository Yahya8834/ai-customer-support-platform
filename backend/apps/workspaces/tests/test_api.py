from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from apps.workspaces.services.create_workspace import CreateWorkspaceService
from apps.workspaces.models import Workspace, WorkspaceMembership, WorkspaceRole
from rest_framework_simplejwt.tokens import RefreshToken



User = get_user_model()


class CreateWorkspaceAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="password123",
        )

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.url = "/api/v1/workspaces/"

    def authenticate(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

    def test_authenticated_user_can_create_workspace(self):
        self.authenticate()

        response = self.client.post(
            self.url,
            {"name": "Acme Support"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workspace.objects.count(), 1)

        workspace = Workspace.objects.get()

        self.assertEqual(workspace.name, "Acme Support")
        self.assertEqual(workspace.slug, "acme-support")

        membership = WorkspaceMembership.objects.get(
            workspace=workspace,
            user=self.user,
        )

        self.assertEqual(membership.role, WorkspaceRole.OWNER)

    def test_unauthenticated_user_cannot_create_workspace(self):
        response = self.client.post(
            self.url,
            {"name": "Acme Support"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Workspace.objects.count(), 0)

    def test_invalid_payload_returns_400(self):
        self.authenticate()

        response = self.client.post(
            self.url,
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

        self.assertEqual(Workspace.objects.count(), 0)

    def test_creator_is_assigned_owner_role(self):
        self.authenticate()

        self.client.post(
            self.url,
            {"name": "My Workspace"},
            format="json",
        )

        membership = WorkspaceMembership.objects.get(user=self.user)

        self.assertEqual(membership.role, WorkspaceRole.OWNER)



    
class ListWorkspacesAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="password123",
        )

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.url = "/api/v1/workspaces/"

    def authenticate(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

    def test_authenticated_user_can_list_their_workspaces(self):
        self.authenticate()

        workspace = Workspace.objects.create(
            name="Acme Support",
            slug="acme-support",
        )

        WorkspaceMembership.objects.create(
            workspace=workspace,
            user=self.user,
            role=WorkspaceRole.OWNER,
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        self.assertEqual(
            response.data[0]["name"],
            "Acme Support",
        )

    def test_user_cannot_see_workspaces_they_do_not_belong_to(self):
        self.authenticate()

        workspace = Workspace.objects.create(
            name="Other Company",
            slug="other-company",
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_unauthenticated_user_cannot_list_workspaces(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )



class AddWorkspaceMemberAPITests(APITestCase):
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

        self.other_user = User.objects.create_user(
            username="other",
            email="other@example.com",
            password="password123",
        )

        self.workspace = CreateWorkspaceService.execute(
            user=self.owner,
            name="Acme Support",
        )

        owner_refresh = RefreshToken.for_user(self.owner)
        self.owner_token = str(owner_refresh.access_token)

        staff_refresh = RefreshToken.for_user(self.staff)
        self.staff_token = str(staff_refresh.access_token)

        self.url = f"/api/v1/workspaces/{self.workspace.uuid}/members/"

    def authenticate(self, token):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )

    def test_owner_can_add_staff_member(self):
        self.authenticate(self.owner_token)

        response = self.client.post(
            self.url,
            {
                "user_uuid": self.staff.uuid,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            WorkspaceMembership.objects.filter(
                workspace=self.workspace,
                user=self.staff,
                role=WorkspaceRole.STAFF,
            ).exists()
        )

    def test_non_owner_cannot_add_staff_member(self):
        self.authenticate(self.staff_token)

        response = self.client.post(
            self.url,
            {
                "user_uuid": self.other_user.uuid,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_unauthenticated_user_cannot_add_staff_member(self):
        response = self.client.post(
            self.url,
            {
                "user_uuid": self.staff.uuid,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_cannot_add_same_staff_member_twice(self):
        self.authenticate(self.owner_token)

        self.client.post(
            self.url,
            {
                "user_uuid": self.staff.uuid,
            },
            format="json",
        )

        response = self.client.post(
            self.url,
            {
                "user_uuid": self.staff.uuid,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            response.data["detail"],
            "User is already a member of this workspace.",
        )


    
    

class ListWorkspaceMembersAPITests(APITestCase):
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

        self.workspace = CreateWorkspaceService.execute(
            user=self.owner,
            name="Acme Support",
        )

        WorkspaceMembership.objects.create(
            workspace=self.workspace,
            user=self.staff,
            role=WorkspaceRole.STAFF,
        )

        refresh = RefreshToken.for_user(self.owner)
        self.owner_token = str(refresh.access_token)

        self.url = f"/api/v1/workspaces/{self.workspace.uuid}/members/"

    def authenticate(self, token):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )

    def test_owner_can_list_workspace_members(self):
        self.authenticate(self.owner_token)
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            2,
        )

        owner = next(
            member
            for member in response.data
            if member["username"] == "owner"
        )

        staff = next(
            member
            for member in response.data
            if member["username"] == "staff"
        )

        self.assertEqual(
            owner["role"],
            WorkspaceRole.OWNER,
        )

        self.assertEqual(
            owner["email"],
            "owner@example.com",
        )

        self.assertEqual(
            staff["role"],
            WorkspaceRole.STAFF,
        )

        self.assertEqual(
            staff["email"],
            "staff@example.com",
        )


    def test_staff_can_list_workspace_members(self):
        self.staff_token = str(
            RefreshToken.for_user(self.staff).access_token
        )

        self.authenticate(self.staff_token)

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            2,
        )

    
    def test_non_member_cannot_list_workspace_members(self):
        outsider = User.objects.create_user(
            username="outsider",
            email="outsider@example.com",
            password="password123",
        )

        outsider_token = str(
            RefreshToken.for_user(outsider).access_token
        )

        self.authenticate(outsider_token)

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )