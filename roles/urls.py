from django.urls import path, include
from roles.views.roles import *
from roles.views.permissions import *

urlpatterns = [
    path('', AllRoles.as_view(), name="view"),
    path('add', AddRoles.as_view(), name="create"),
    path('<int:pk>/delete', DeleteRoles.as_view(), name="delete"),
    path('<int:pk>/update', UpdateRoles.as_view(), name="update"),
    path('<int:pk>/permission/', include(("roles.permission_urls", "roles"), namespace="permission"))
]
