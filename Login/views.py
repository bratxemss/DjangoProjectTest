from django.contrib.auth import authenticate
from django.shortcuts import render, redirect





def main(request):
    return render(request, 'login/main.html')

def login(request):
    return render(request, 'login/login.html')

def register(request):
    return render(request, 'login/register.html')



