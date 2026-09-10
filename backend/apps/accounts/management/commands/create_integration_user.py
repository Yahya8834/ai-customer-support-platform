from django.core.management.base import BaseCommand
from apps.accounts.models import User



class Command(BaseCommand):
    help = "Create the user used by frontend integration tests."

    def handle(self, *args, **options):
        User.objects.get_or_create(
            username="frontend-integration-user",
            defaults={
                "email": "frontend-integration@example.com",
            },
        )

        user = User.objects.get(username="frontend-integration-user")
        user.set_password("FrontendIntegration123!")
        user.save(update_fields=["password"])

        self.stdout.write(
            self.style.SUCCESS(
                "Frontend integration user is ready."
            )
        )