from functools import wraps
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.urls import reverse


def check_user_permission(code_name):
    def wrapper(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            if not request.user.is_superuser:
                try:
                    check_permission = request.user.role.rolepermissions_set.filter(permission__codename=code_name)
                    if check_permission:
                        return func(request, *args, **kwargs)
                    return redirect(reverse("dashboard:home"))
                except:
                    return redirect(reverse("dashboard:home"))
            else:
                return func(request, *args, **kwargs)

        return inner

    return wrapper


def class_view_decorator(function_decorator):
    def deco(View):
        View.dispatch = method_decorator(function_decorator)(View.dispatch)
        return View

    return deco
