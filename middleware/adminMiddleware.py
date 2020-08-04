from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import reverse
import re


class AdminMiddleware(MiddlewareMixin):

    def process_request(self, request):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')
        if re.compile(r'^admin+').match(path):
            if request.user.is_authenticated:
                if not request.user.is_superuser:
                    return redirect(reverse("dashboard:home"))
            else:
                if not path == "admin/login":
                    return redirect(reverse("admin_login"))
