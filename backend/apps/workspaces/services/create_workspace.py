from django.db import transaction
from apps.workspaces.utils import generate_workspace_slug

from apps.workspaces.models import (
    Workspace,
    WorkspaceMembership,
    WorkspaceRole,
)


class CreateWorkspaceService:
    
    @staticmethod
    @transaction.atomic
    def execute(*, user, name: str) -> Workspace:
        workspace = Workspace.objects.create(
        name=name,
        slug=generate_workspace_slug(name),
        )   
        WorkspaceMembership.objects.create(
            workspace=workspace,
            user=user,
            role=WorkspaceRole.OWNER,
        )

        return workspace