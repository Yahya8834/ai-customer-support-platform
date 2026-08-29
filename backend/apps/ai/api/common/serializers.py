from rest_framework import serializers

from apps.ai.models import LLMModel


class LLMModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLMModel
        fields = (
            "key",
            "display_name",
            "description",
            "strength",
            "provider",
            "model_name",
            "input_price_per_1k_tokens",
            "output_price_per_1k_tokens",
        )