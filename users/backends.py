from users.models import Users, Passwords
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import AnonymousUser


class CustomUserAuth(BaseBackend):

    def authenticate(self, request, username=None, password=None):
        try:
            user = Users.objects.get(name=username)
            user_id = user.pk
            password_obj = Passwords
            password_verify = password_obj.objects.verify_password(password, user_id)
            if password_verify["success"]:
                return user
            else:
                return None

        except Users.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = Users.objects.get(pk=user_id)
            if user.is_active:
                return user
            return AnonymousUser()
        except Users.DoesNotExist:
            return AnonymousUser()
