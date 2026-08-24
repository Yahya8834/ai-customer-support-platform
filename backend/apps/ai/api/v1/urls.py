from django.urls import path
from .views import AvailableLLMModelsView



urlpatterns = [
    path(
        "v1/llm-models/",
        AvailableLLMModelsView.as_view(),
        name="available-llm-models",
    ),
]