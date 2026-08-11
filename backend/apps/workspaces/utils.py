from django.utils.text import slugify

from apps.workspaces.models import Workspace


def generate_workspace_slug(name: str) -> str:
    base_slug = slugify(name)
    slug = base_slug
    counter = 2

    while Workspace.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug