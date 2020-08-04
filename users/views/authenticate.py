from django.shortcuts import render
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse
from users.views.password_encryption_decryption import Password
from django.urls import reverse


def login(request):
    try:
        password_hash = Password()
        if request.method == "POST":

            request_data = request.POST
            user_name = request_data["username"]
            password = request_data["password"]
            password = password_hash.decode_password(password)
            auth_try = authenticate(request, username=user_name, password=password)
            if auth_try:
                auth_login(request, auth_try)
                request.session["username"] = auth_try.name
                request.user = auth_try
                return JsonResponse({"success": True, "redirect": settings.LOGIN_REDIRECT_URL})
            else:
                return JsonResponse({"success": False, "msg": "Credentials not Verified"})

        elif request.method == "GET":
            public_key = password_hash.get_public_key()
            if request.user.is_authenticated:
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                if check_admin():
                    return render(request, "users/login.html", {"rsa_key": public_key})
                else:
                    return redirect(reverse("setup"))

    except Exception as e:
        print(e)
        return JsonResponse({"success": False, "msg": "Some Error Occurred Please Contact Admin"})


def logout(request):
    if request.user.is_active:
        auth.logout(request)
        return redirect("/user/login", messages.error(request, "Successfully Logged Out"))


def check_admin():
    from users.models import Users
    user = Users.objects.filter(is_superuser=False)
    if not user:
        return False
    else:
        return True
