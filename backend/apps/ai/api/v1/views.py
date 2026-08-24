from rest_framework.response import Response
from rest_framework.views import APIView
from apps.ai.api.common.serializers import LLMModelSerializer
from apps.ai.models import LLMModel
from rest_framework.permissions import IsAuthenticated


class AvailableLLMModelsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        models = LLMModel.objects.filter(
            is_active=True,
        )

        serializer = LLMModelSerializer(
            models,
            many=True,
        )

        return Response(
            {
                "models": serializer.data,
            }
        )