from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .forms import LoginForm


@api_view(['POST'])
def login_view(request):
    form = LoginForm(request.data)

    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            response = Response({"message": "Login successful"}, status=200)
            response.set_cookie(
                "access_token", str(refresh.access_token), httponly=True, samesite="Lax"
            )
            return response
        else:
            return Response({"error": "Incorrect credentials"}, status=400)
    else:
        return Response({"error": "Invalid form data"}, status=400)