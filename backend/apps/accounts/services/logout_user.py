from rest_framework_simplejwt.tokens import RefreshToken


class LogoutUserService:
    def execute(self, refresh_token: str) -> None:
        token = RefreshToken(refresh_token)
        token.blacklist()