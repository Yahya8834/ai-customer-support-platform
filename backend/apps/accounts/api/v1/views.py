import uuid
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.accounts.services.logout_user import LogoutUserService
from apps.accounts.api.common.serializers import (
    RegisterUserSerializer,
    UserSerializer,
    LogoutSerializer,
)
from apps.accounts.services.register_user import RegisterUserService


User = get_user_model()


class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = RegisterUserService().execute(**serializer.validated_data)

        return Response(
            {
                "uuid": user.uuid,
                "username": user.username,
                "email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )


class MeAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        LogoutUserService().execute(
            serializer.validated_data["refresh"]
        )

        return Response(status=status.HTTP_204_NO_CONTENT)