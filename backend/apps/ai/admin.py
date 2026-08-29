from django.contrib import admin
from .models import LLMModel


@admin.register(LLMModel)
class LLMModelAdmin(admin.ModelAdmin):
    list_display = (
        "display_name",
        "key",
        "strength",
        "input_price_per_1k_tokens",
        "output_price_per_1k_tokens",
        "is_active",
    )
    list_filter = ("is_active",)
    search_fields = ("display_name", "key")