from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from apps.ai.models import LLMModel
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken



User = get_user_model()



class AvailableLLMModelsAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user",
            email="user@example.com",
            password="password123",
        )

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

    def test_returns_active_models(self):
        LLMModel.objects.create(
            key="deepseek",
            display_name="DeepSeek",
            description="Strong reasoning model",
            strength="Reasoning",
            provider="deepseek",
            model_name="deepseek-chat",
            input_price_per_1k_tokens=0,
            output_price_per_1k_tokens=0,
            is_active=True,
        )

        LLMModel.objects.create(
            key="inactive-model",
            display_name="Inactive Model",
            description="Unavailable model",
            strength="Basic",
            provider="deepseek",
            model_name="deepseek-chat",
            input_price_per_1k_tokens=0,
            output_price_per_1k_tokens=0,
            is_active=False,
        )

        response = self.client.get("/api/v1/llm-models/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["models"],
            [
                {
                    "key": "deepseek",
                    "display_name": "DeepSeek",
                    "description": "Strong reasoning model",
                    "strength": "Reasoning",
                    "provider": "deepseek",
                    "model_name": "deepseek-chat",
                    "input_price_per_1k_tokens": "0.000000",
                    "output_price_per_1k_tokens": "0.000000",
                }
            ],
        ) 

    
    def test_unauthenticated_user_cannot_view_models(self):
        self.client.credentials()
        response = self.client.get(
            "/api/v1/llm-models/",
        )

        self.assertEqual(response.status_code, 401)


    def test_inactive_models_are_not_returned(self):
        LLMModel.objects.create(
            key="inactive-model",
            display_name="Inactive Model",
            description="Unavailable model",
            strength="Basic",
            provider="deepseek",
            model_name="deepseek-chat",
            input_price_per_1k_tokens=0,
            output_price_per_1k_tokens=0,
            is_active=False,
        )

        response = self.client.get(
            "/api/v1/llm-models/",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["models"], [])


