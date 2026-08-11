from django.urls import include, path
from apps.accounts.api.v1.views import MeAPIView, RegisterUserAPIView, LogoutAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("v1/register/", RegisterUserAPIView.as_view(), name="register"),
    path("v1/login/", TokenObtainPairView.as_view(), name="login"),
    path("v1/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("v1/me/", MeAPIView.as_view(), name="me"),
    path("v1/logout/", LogoutAPIView.as_view(), name="logout"),
]
 