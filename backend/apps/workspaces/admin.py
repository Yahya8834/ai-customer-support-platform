from django.contrib import admin

from apps.workspaces.models import (
    Workspace,
    WorkspaceMembership,
)


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "name",
        "slug",
    )

    ordering = (
        "-created_at",
    )


@admin.register(WorkspaceMembership)
class WorkspaceMembershipAdmin(admin.ModelAdmin):
    list_display = (
        "workspace",
        "user",
        "role",
        "created_at",
    )

    list_filter = (
        "role",
        "created_at",
    )

    search_fields = (
        "workspace__name",
        "user__email",
    )

    ordering = (
        "-created_at",
    )