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

from Login.views import login, register, main
from Login.api import login_view, register_user, check_code, exit

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/exit', exit, name='exit'),
    path('api/login/', login_view, name='api_login'),
    path('api/register/', register_user, name='register_user'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/check_code', check_code, name='verify_code'),

    path('login/', login, name='login_page'),
    path('register/', register, name='register_page'),
    path('', main, name='main_page'),

]