from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


def create_and_save_token(user):
    refresh = RefreshToken.for_user(user)
    response = Response({"message": "Successful entry"})
    response.set_cookie("access_token", str(refresh.access_token), httponly=True, samesite="Lax")
    return response