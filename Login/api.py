from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken

from .forms import LoginForm, RegisterForm


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


@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    password_copy = request.data.get('password_copy')

    print(request.data)
    if not username or not email or not password or not password_copy:
        return Response({"error": "Все поля обязательны для заполнения"}, status=status.HTTP_400_BAD_REQUEST)

    if password != password_copy:
        return Response({"error": "Пароли не совпадают"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Имя пользователя уже занято"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email уже используется"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        validate_password(password)
    except ValidationError as e:
        return Response({"error": f"Пароль не соответствует требованиям: {', '.join(e.messages)}"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    refresh = RefreshToken.for_user(user)
    response = Response({
        "message": "Пользователь успешно зарегистрирован",
    }, status=status.HTTP_201_CREATED)

    response.set_cookie(
        "access_token", str(refresh.access_token), httponly=True, samesite="Lax"
    )
    print("REGISTR!")
    return response