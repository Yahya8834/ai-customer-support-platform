from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class RegisterUserAPITest(APITestCase):
    def test_register_user_successfully(self):
        payload = {
            "username": "john",
            "email": "john@example.com",
            "password": "StrongPassword123!",
        }
        response = self.client.post(
            "/api/v1/register/",
            payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        user = User.objects.first()

        self.assertEqual(user.username, payload["username"])
        self.assertEqual(user.email, payload["email"])
        self.assertTrue(user.check_password(payload["password"]))

        self.assertNotIn("password", response.data)


    def test_cannot_register_with_duplicate_email(self):
        User.objects.create_user(
            username="john",
            email="john@example.com",
            password="StrongPassword123!",
        )
        payload = {
            "username": "john2",
            "email": "john@example.com",
            "password": "StrongPassword123!",
        }
        response = self.client.post("/api/v1/register/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)


    def test_cannot_register_with_invalid_email(self):
        payload = {
            "username": "john",
            "email": "not-an-email",
            "password": "StrongPassword123!",
        }
        response = self.client.post("/api/v1/register/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)


    def test_cannot_register_with_short_password(self):
        payload = {
            "username": "john",
            "email": "john@example.com",
            "password": "123",
        }
        response = self.client.post("/api/v1/register/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_cannot_register_with_missing_fields(self):
        payload = {}
        response = self.client.post("/api/v1/register/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)


    def test_login_returns_access_and_refresh_tokens(self):
        User.objects.create_user(
            username="john",
            email="john@example.com",
            password="StrongPassword123!",
        )
        response = self.client.post(
            "/api/v1/login/",
            {
                "username": "john",
                "password": "StrongPassword123!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    
    def test_login_with_invalid_credentials_returns_401(self):
        User.objects.create_user(
            username="john",
            email="john@example.com",
            password="StrongPassword123!",
        )
        response = self.client.post(
            "/api/v1/login/",
            {
                "username": "john",
                "password": "WrongPassword123!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    
    def test_authenticated_user_can_access_me_endpoint(self):
        user = User.objects.create_user(
            username="john",
            email="john@example.com",
            password="StrongPassword123!",
        )
        login_response = self.client.post(
            "/api/v1/login/",
            {
                "username": "john",
                "password": "StrongPassword123!",
            },
            format="json",
        )
        access_token = login_response.data["access"]
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )
        response = self.client.get("/api/v1/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uuid"], str(user.uuid))
        self.assertEqual(response.data["username"], user.username)
        self.assertEqual(response.data["email"], user.email)


    
    def test_unauthenticated_user_cannot_access_me_endpoint(self):
        response = self.client.get("/api/v1/me/")
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )