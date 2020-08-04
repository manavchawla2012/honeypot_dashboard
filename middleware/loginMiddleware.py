from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.conf import settings
from users.models import Users
import re

EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]


class Login(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        pass

    def process_request(self, request):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')
        if not request.user.is_authenticated:
            if not any(url.match(path) for url in EXEMPT_URLS):
                return redirect(settings.LOGIN_URL)
            else:
                if path == "user/setup" and Users.objects.filter(is_superuser=False):
                    return redirect(settings.LOGIN_URL)

