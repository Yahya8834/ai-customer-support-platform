from django.db import IntegrityError
from django.test import TestCase
from apps.ai.models import LLMModel



class LLMModelTests(TestCase):
    def test_key_must_be_unique(self):
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

        with self.assertRaises(IntegrityError):
            LLMModel.objects.create(
                key="deepseek",
                display_name="Another DeepSeek",
                description="Another model",
                strength="Reasoning",
                provider="deepseek",
                model_name="another-model",
                input_price_per_1k_tokens=0,
                output_price_per_1k_tokens=0,
                is_active=True,
            )