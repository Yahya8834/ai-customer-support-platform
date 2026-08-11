from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import PermissionDenied
from apps.workspaces.models import (
    Workspace,
    WorkspaceMembership,
    WorkspaceRole,
)
from apps.common.exceptions import AlreadyWorkspaceMemberError
from apps.workspaces.services.create_workspace import CreateWorkspaceService
from apps.workspaces.services.add_workspace_member import AddWorkspaceMemberService
from apps.workspaces.services.list_workspace_members import ListWorkspaceMembersService

User = get_user_model()


class CreateWorkspaceServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="password123",
        )

    def test_creates_workspace_and_owner_membership(self):
        workspace = CreateWorkspaceService.execute(
            user=self.user,
            name="Acme Support",
        )

        self.assertEqual(Workspace.objects.count(), 1)
        self.assertEqual(workspace.name, "Acme Support")

        membership = WorkspaceMembership.objects.get(
            workspace=workspace,
            user=self.user,
        )

        self.assertEqual(membership.role, WorkspaceRole.OWNER)

    def test_generates_unique_slug_for_duplicate_workspace_names(self):
        first = CreateWorkspaceService.execute(
            user=self.user,
            name="Acme Support",
        )

        second_user = User.objects.create_user(
            username="staff",
            email="staff@example.com",
            password="password123",
        )

        second = CreateWorkspaceService.execute(
            user=second_user,
            name="Acme Support",
        )

        self.assertEqual(first.slug, "acme-support")
        self.assertEqual(second.slug, "acme-support-2")




class AddWorkspaceMemberServiceTests(TestCase):
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

    
    def test_owner_can_add_staff_member(self):
        membership = AddWorkspaceMemberService.execute(
            actor=self.owner,
            workspace=self.workspace,
            user=self.staff,
        )

        self.assertEqual(membership.role, WorkspaceRole.STAFF)
        self.assertTrue(
            WorkspaceMembership.objects.filter(
                workspace=self.workspace,
                user=self.staff,
                role=WorkspaceRole.STAFF,
            ).exists()
        )


    def test_non_owner_cannot_add_staff_member(self):
        with self.assertRaises(PermissionDenied):
            AddWorkspaceMemberService.execute(
                actor=self.staff,
                workspace=self.workspace,
                user=self.staff,
            )

    def test_cannot_add_same_staff_member_twice(self):
        AddWorkspaceMemberService.execute(
            actor=self.owner,
            workspace=self.workspace,
            user=self.staff,
        )
        with self.assertRaises(AlreadyWorkspaceMemberError):
            AddWorkspaceMemberService.execute(
                actor=self.owner,
                workspace=self.workspace,
                user=self.staff,
            )



class ListWorkspaceMembersServiceTests(TestCase):
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

    def test_owner_can_list_workspace_members(self):
        memberships = ListWorkspaceMembersService.execute(
            actor=self.owner,
            workspace=self.workspace,
        )

        self.assertEqual(memberships.count(), 2)

        self.assertTrue(
            memberships.filter(
                user=self.owner,
                role=WorkspaceRole.OWNER,
            ).exists()
        )

        self.assertTrue(
            memberships.filter(
                user=self.staff,
                role=WorkspaceRole.STAFF,
            ).exists()
        )


    def test_non_member_cannot_list_workspace_members(self):
        outsider = User.objects.create_user(
            username="outsider",
            email="outsider@example.com",
            password="password123",
        )

        with self.assertRaises(PermissionDenied):
            ListWorkspaceMembersService.execute(
                actor=outsider,
                workspace=self.workspace,
            )