from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from datetime import datetime
import hashlib
from roles.models import Roles
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):

    def _create_user(self, email, name, first_name, password, **kwargs):
        now = datetime.now()
        user = name
        email = email
        password = password
        first_name = first_name
        user = self.model(name=user, email_id=email, first_name=first_name, created_at=now,
                          updated_at=now, **kwargs)
        user.set_unusable_password()
        user.save()
        encrypt_password = hashlib.sha1(password.encode("utf-8")).hexdigest()
        password = Passwords.objects.create(hashed_password=encrypt_password, days_to_expire=999, is_active=1,
                                            created_at=now, updated_at=now, user=user)
        password.save()
        print("User Created Successfully")

    def create_user(self, email, name, first_name, password, **kwargs):
        return self._create_user(email, name, first_name, password, **kwargs)

    def verify_password(self, raw_password, user_id):
        password = Passwords
        data = self._get_latest_password(user_id, password)
        if not data:
            return {"success": False, "msg": "Password Not found Please Contact Administrator "}
        else:
            encrypt_password = hashlib.sha1(raw_password.encode("utf-8")).hexdigest()
            if encrypt_password == data["hashed_password"]:
                return {"success": True, "msg": "Password Match"}
            else:
                return {"success": False, "msg": "Password Fail"}

    def update_user(self, user, password):
        user.updated_at = datetime.now()
        user.save()
        if password:
            encrypt_password = hashlib.sha1(password.encode("utf-8")).hexdigest()

    def _get_latest_password(self, user_id, pass_obj):
        password_data = pass_obj.objects.filter(user_id=user_id, is_active=1).values().first()
        return password_data


class Users(AbstractBaseUser, PermissionsMixin):
    email_id = models.EmailField(
        verbose_name='email address',
        max_length=255,
    )
    name = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_locked = models.BooleanField(default=False)
    role = models.ForeignKey(Roles, on_delete=models.DO_NOTHING, null=True)
    login_expiry = models.DateTimeField(null=True)
    is_superuser = models.BooleanField(default=False, null=False)
    password = None
    last_login = models.DateTimeField(null=True)
    created_at = models.DateTimeField(default=timezone.now, null=False, blank=False)
    updated_at = models.DateTimeField(null=False, blank=False, default=timezone.now)

    USERNAME_FIELD = 'name'
    objects = UserManager()

    class Meta:
        db_table = "users"
        app_label = "users"

    def get_username(self):
        return self.name

    def __str__(self):
        return self.email_id

    @property
    def is_locked(self):
        return self.is_locked


class Passwords(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    hashed_password = models.CharField(max_length=64, verbose_name='password')
    days_to_expire = models.IntegerField()
    is_active = models.BooleanField()
    created_at = models.DateTimeField(default=timezone.now, null=False, blank=False)
    updated_at = models.DateTimeField(null=False, blank=False, default=timezone.now)
    objects = UserManager()

    class Meta:
        db_table = "passwords"
        app_label = "users"
