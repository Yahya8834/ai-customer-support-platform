from django.core.management.base import BaseCommand

from apps.ai.models import LLMModel


class Command(BaseCommand):
    help = "Seed the supported V1 LLM models."

    def handle(self, *args, **options):
        models = [
            {
                "key": "local-deepseek",
                "display_name": "DeepSeek R1 8B",
                "description": "Local DeepSeek R1 8B model served by Ollama.",
                "strength": "Reasoning",
                "provider": "ollama",
                "model_name": "deepseek-r1:8b",
                "input_price_per_1k_tokens": 0,
                "output_price_per_1k_tokens": 0,
                "is_active": False,
            },
            {
                "key": "cloud-qwen",
                "display_name": "Qwen 3.5 397B A17B",
                "description": "Cloud Qwen 3.5 model served by DigitalOcean inference.",
                "strength": "General purpose",
                "provider": "qwen",
                "model_name": "qwen3.5-397b-a17b",
                "input_price_per_1k_tokens": 0.000550,
                "output_price_per_1k_tokens": 0.003500,
                "is_active": False,
            },
        ]

        for model_data in models:
            LLMModel.objects.update_or_create(
                key=model_data["key"],
                defaults=model_data,
            )

        self.stdout.write(
            self.style.SUCCESS("LLM models seeded successfully.")
        )