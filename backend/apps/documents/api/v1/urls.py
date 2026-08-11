from django.urls import path
from .views import DocumentsView, RetrieveDocumentView

app_name = "documents"

urlpatterns = [
    path(
        "v1/workspaces/<uuid:workspace_uuid>/documents/",
        DocumentsView.as_view(),
        name="workspace-documents",
    ),
    path(
        "v1/workspaces/<uuid:workspace_uuid>/documents/<uuid:document_uuid>/",
        RetrieveDocumentView.as_view(),
        name="workspace-document-detail",
    ),
]