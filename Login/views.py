from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import create_and_save_token


@api_view(['POST'])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    from django.contrib.auth import authenticate
    user = authenticate(username=username, password=password)

    if user is not None:
        create_and_save_token(user)
        return render(request, 'login/main.html')
    return Response({"error": "Incorrect credentials"}, status=400)

def login(request):
    return render(request, 'login/login.html')

def register(request):
    return render(request, 'login/register.html')

def forgot_password(request):
    return render(request, 'login/forgot-password.html')


