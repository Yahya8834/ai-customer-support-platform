from django.urls import path

from apps.workspaces.api.v1.views import (
    AddWorkspaceMemberView,
    WorkspaceListCreateView,
)



urlpatterns = [
    path(
        "v1/workspaces/",
        WorkspaceListCreateView.as_view(),
        name="workspace-list-create",
    ),
    path(
        "v1/workspaces/<uuid:workspace_uuid>/members/",
        AddWorkspaceMemberView.as_view(),
        name="workspace-add-member",
    ),
]