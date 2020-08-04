from django.urls import path, include, reverse_lazy
from admin.views import admin_login, admin_home, logout
from django.views.generic import RedirectView

urlpatterns = [
    path("login", admin_login, name="admin_login"),
    path("home", admin_home, name="admin_home"),
    path('logout', logout, name="admin_logout"),
    path("", RedirectView.as_view(url=reverse_lazy("admin_home")))
]
