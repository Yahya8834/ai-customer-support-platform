from apps.workspaces.models import Workspace


def get_user_workspaces(user):
    return (
        Workspace.objects.filter(
            memberships__user=user,
        )
        .distinct()
        .order_by("name")
    )