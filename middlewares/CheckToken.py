from django.shortcuts import redirect
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken
from django.urls import resolve, Resolver404


class CheckAccessTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        access_token = request.COOKIES.get('access_token')
        current_page = request.path

        if access_token:
            try:
                resolve(current_page)
                try:
                    AccessToken(access_token)
                    if 'auth' in current_page:
                        return redirect('main_page')
                except (InvalidToken, TokenError):
                    return redirect('main_page')
            except Resolver404:
                return redirect('login_page')

        elif 'auth' not in current_page and 'admin' not in current_page and 'api' not in current_page :
            return redirect('login_page')

        response = self.get_response(request)
        return response
