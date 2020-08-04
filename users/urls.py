from django.urls import path
from users.views.authenticate import login, logout
from users.views.userOperations import CreateUser, UpdateUser, AllUsers, DeleteUser, DetailUser, Setup

urlpatterns = [
    path("login", login, name="user_login"),
    path("logout", logout, name="user_logout"),
    path("new", CreateUser.as_view(), name="create_users"),
    path("<int:pk>", DetailUser.as_view(), name="detail_users"),
    path("<int:pk>/update", UpdateUser.as_view(), name="change_users"),
    path("<int:pk>/delete", DeleteUser.as_view(), name="delete_users"),
    path("setup", Setup.as_view(), name="setup"),
    path('', AllUsers.as_view(), name="view_users")
]
