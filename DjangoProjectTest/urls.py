"""
URL configuration for DjangoProjectTest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from Login.views import login, register, forgot_password, main
from Login.api import login_view

urlpatterns = [
    path('admin/', admin.site.urls),


    path('api/login/', login_view, name='api_login'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('auth/login/', login, name='login_page'),
    path('auth/register/', register, name='register_page'),
    path('auth/forgot_password/', forgot_password, name='forgot_password_page'),
    path('', main, name='main_page'),

]