from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from .forms import LoginForm, RegisterForm
from .tasks import send_code_to_email
from .models import ConfirmationCode


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
    form = RegisterForm(request.data)
    if form.is_valid():
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        password_copy = request.data.get('password_copy')

        print(request.data)
        if not username or not email or not password or not password_copy:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if password != password_copy:
            return Response({"error": "The passwords don't match"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "The username is already taken"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email is already in use"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"error": f"Password does not meet the requirements: {', '.join(e.messages)}"}, status=status.HTTP_400_BAD_REQUEST)


        send_code_to_email.delay(email)
        return Response({"message":"success"},status=status.HTTP_201_CREATED)

    return Response({"error": f"Not valid form"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def check_code(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    code = request.data.get('code')

    if ConfirmationCode.objects.filter(code=code, email=email):
        user = User.objects.create_user(username=username, email=email, password=password)
        refresh = RefreshToken.for_user(user)
        response = Response({
            "success": True,
        }, status=status.HTTP_201_CREATED)

        response.set_cookie(
            "access_token", str(refresh.access_token), httponly=True, samesite="Lax"
        )
        ConfirmationCode.objects.filter(email=email, code=code).first().delete()
        return response
    else:
        return Response({
            "error": "no user",
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def exit(request):

    response = Response({"success": True}, status=status.HTTP_200_OK)
    response.delete_cookie('access_token')

    return response