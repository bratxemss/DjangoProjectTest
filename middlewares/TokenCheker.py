from django.shortcuts import redirect


class CheckAccessTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        access_token = request.COOKIES.get('access_token')
        current_page = request.path

        if not access_token and current_page != '/login' and 'admin' not in current_page:
            return redirect('/login')

        response = self.get_response(request)
        return response
