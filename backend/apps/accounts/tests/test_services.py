from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.services.logout_user import LogoutUserService
from apps.accounts.services.register_user import RegisterUserService
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
User = get_user_model()


class RegisterUserServiceTest(TestCase):
    def test_register_user_creates_user(self):
        user = RegisterUserService().execute(
            username="john",
            email="john@example.com",
            password="StrongPassword123!",
        )

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, "john")
        self.assertEqual(user.email, "john@example.com")
        self.assertTrue(user.check_password("StrongPassword123!"))

    def test_password_is_hashed(self):
        user = RegisterUserService().execute(
            username="john",
            email="john@example.com",
            password="StrongPassword123!",
        )

        self.assertNotEqual(user.password, "StrongPassword123!")
        self.assertTrue(user.check_password("StrongPassword123!"))


class LogoutUserServiceTest(TestCase):
    def test_logout_blacklists_refresh_token(self):
        user = User.objects.create_user(
            username="john",
            email="john@example.com",
            password="StrongPassword123!",
        )

        refresh = RefreshToken.for_user(user)
        LogoutUserService().execute(str(refresh))
        self.assertEqual(BlacklistedToken.objects.count(), 1)