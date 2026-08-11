from django.contrib.auth import get_user_model
from django.db import transaction
from apps.common.exceptions import BusinessLogicError


User = get_user_model()


class RegisterUserService:
    """Handles user registration."""

    @transaction.atomic
    def execute(self, *, username: str, email: str, password: str) -> User:
        if User.objects.filter(email=email).exists():
            raise BusinessLogicError("A user with this email already exists.")
        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )