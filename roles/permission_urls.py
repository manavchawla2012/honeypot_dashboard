from django.urls import path
from roles.views.permissions import *


urlpatterns = [
    path("", ViewRolePermissions.as_view(), name="view"),
    path("add", AddRolePermissions.as_view(), name="create"),
    path("delete/<int:permissionId>", DeleteRolePermissions.as_view(), name="delete")
]