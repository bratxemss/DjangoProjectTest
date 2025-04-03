from django.shortcuts import render

def login(request):
    return render(request, 'login/login.html')

def register(request):
    return render(request, 'login/register.html')

def forgot_password(request):
    return render(request, 'login/forgot-password.html')


