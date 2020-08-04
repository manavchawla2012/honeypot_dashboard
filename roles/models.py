from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


# Create your models here.


class Roles(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=1000, null=True)
    created_at = models.DateTimeField(blank=False, null=False, default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True, default=timezone.now)

    class Meta:
        managed = True
        db_table = "roles"

    def __str__(self):
        return self.name


class RolePermissions(models.Model):
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, default=None)

    created_at = models.DateTimeField(blank=False, null=False, default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True, default=timezone.now)

    class Meta:
        managed = True
        db_table = "role_permissions"
        unique_together = ('role', 'permission')
        constraints = [
            models.UniqueConstraint(fields=['role', 'permission'], name="unique_role_permission")
        ]

    def __str__(self):
        return self.permission.name
