from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from roles.models import RolePermissions, Roles
from roles.forms.new import NewRolePermission
from decorators.check_module_permissions import check_user_permission, class_view_decorator


@class_view_decorator(check_user_permission("view_rolepermissions"))
class ViewRolePermissions(ListView):
    model = RolePermissions
    template_name = "roles_permissions/permissions.html"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        role_id = self.kwargs.get("pk")
        context_data = super(ViewRolePermissions, self).get_context_data()
        context_data["role_id"] = role_id
        return context_data

    def get_queryset(self):
        role_id = self.kwargs.get("pk")
        queryset = RolePermissions.objects.filter(role=role_id).order_by("pk")
        return queryset


@class_view_decorator(check_user_permission("add_rolepermissions"))
class AddRolePermissions(CreateView):
    model = RolePermissions
    template_name = "roles_permissions/new_permission.html"
    form_class = NewRolePermission

    def form_valid(self, form):
        role_id = self.kwargs.get("pk")
        form.save(role_id=role_id)
        return redirect(reverse("roles:permission:view", args=(role_id,)))

    def get_context_data(self, **kwargs):
        role_id = self.kwargs.get("pk")
        context_data = super(AddRolePermissions, self).get_context_data()
        context_data["role_id"] = role_id
        context_data["form"].fields["role_id"].initial = role_id
        return context_data


@class_view_decorator(check_user_permission("delete_rolepermissions"))
class DeleteRolePermissions(DeleteView):
    model = RolePermissions
    pk_url_kwarg = "permissionId"
    template_name = "roles_permissions/delete.html"

    def get_success_url(self):
        return reverse("roles:permission:view", args=(self.kwargs.get("pk"),))

