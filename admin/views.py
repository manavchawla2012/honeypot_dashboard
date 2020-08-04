from django.shortcuts import render
from users.views.password_encryption_decryption import Password
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import auth, messages


# Create your views here.


def admin_login(request):
    try:
        password_hash = Password()
        if request.method == "POST":

            request_data = request.POST
            user_name = request_data["username"]
            password = request_data["password"]
            password = password_hash.decode_password(password)
            auth_try = authenticate(request, username=user_name, password=password)
            if auth_try:
                request.session["username"] = auth_try.name
                request.user = auth_try
                if request.user.is_superuser == 1:
                    auth_login(request, auth_try)
                    return JsonResponse({"success": True, "redirect": reverse("admin_home")})
                else:
                    return JsonResponse({"success": False, "msg": "Not Admin User"})
            else:
                return JsonResponse({"success": False, "msg": "Credentials not Verified"})

        elif request.method == "GET":
            create_new_user_if_not_present()
            public_key = password_hash.get_public_key()
            if request.user.is_authenticated:
                return redirect(reverse("admin_home"))
            else:
                return render(request, "admin/login.html", {"rsa_key": public_key})

    except Exception as e:
        print(e)
        return JsonResponse({"success": False, "msg": "Some Error Occurred Please Contact Admin"})


def admin_home(request):
    return render(request, "admin/home.html")


def logout(request):
    if request.user.is_active:
        auth.logout(request)
        return redirect(reverse("admin_login"), messages.error(request, "Successfully Logged Out"))


def create_new_user_if_not_present():
    from users.models import Users
    user = Users.objects.all()
    if not user:
        Users.objects.create_user(name="subexuser", email="test@subex.com", first_name="SubexUser",
                                  password="Subex@123", is_superuser=True)
